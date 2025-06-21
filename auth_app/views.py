from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from urllib.parse import urlparse
import sys
import os
import json
from datetime import datetime

# Import scraper-ul
try:
    # Try multiple possible paths for the scraper
    import sys
    import os
    
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try different possible paths
    possible_paths = [
        os.path.join(current_dir, '..', 'scripts'),  # Relative from auth_app
        os.path.join(current_dir, '..', '..', 'scripts'),  # Relative from auth_app
        '/code/scripts',  # Absolute path in Docker container
        os.path.join(os.getcwd(), 'scripts'),  # From current working directory
    ]
    
    scraper_imported = False
    for path in possible_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, 'NOD1.py')):
            if path not in sys.path:
                sys.path.insert(0, path)
            try:
                from NOD1 import UniversalSuperScraper
                SCRAPER_AVAILABLE = True
                scraper_imported = True
                print(f"✅ Scraper imported successfully from: {path}")
                break
            except ImportError as e:
                print(f"❌ Failed to import from {path}: {e}")
                continue
    
    if not scraper_imported:
        raise ImportError("Could not import scraper from any of the attempted paths")
        
except ImportError as e:
    SCRAPER_AVAILABLE = False
    print(f"Scraper Import Warning: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Current file directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Python path: {sys.path}")

from .models import ScrapedSite, ScrapedData, AIPersona
from .forms import ScrapingForm

# OpenAI Configuration
try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    OPENAI_AVAILABLE = bool(openai.api_key)
except:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI API key not configured. AI Personas functionality will be limited.")

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('auth_app:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bine ai venit, {username}!')
                return redirect('auth_app:dashboard')
            else:
                messages.error(request, 'Username sau parolă incorectă.')
        else:
            messages.error(request, 'Vă rugăm să corectați erorile de mai jos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth_app/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'Ați fost deconectat cu succes.')
    return redirect('auth_app:login')

@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    recent_sites = ScrapedSite.objects.filter(user=request.user)[:5]
    recent_personas = AIPersona.objects.filter(user=request.user)[:5]
    
    context = {
        'recent_sites': recent_sites,
        'recent_personas': recent_personas,
        'total_sites': ScrapedSite.objects.filter(user=request.user).count(),
        'total_personas': AIPersona.objects.filter(user=request.user).count(),
        'scraper_available': SCRAPER_AVAILABLE,
    }
    return render(request, 'auth_app/dashboard.html', context)

@login_required
def generate_personas_from_site(request, site_id):
    """
    Generates AI personas based on the scraped data of a specific site.
    """
    if not OPENAI_AVAILABLE:
        messages.error(request, 'Funcționalitatea AI nu este disponibilă. Verifică cheia API OpenAI.')
        return redirect('auth_app:site_detail', site_id=site_id)

    try:
        site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
        data = site.scrapeddata_set.first()
        if not data:
            messages.error(request, 'Nu există date scanate pentru acest site. Nu se pot genera personas.')
            return redirect('auth_app:site_detail', site_id=site_id)
    except ScrapedSite.DoesNotExist:
        messages.error(request, 'Site-ul specificat nu a fost găsit.')
        return redirect('auth_app:site_list')

    # Construct a detailed prompt from scraped data
    scraped_info = f"""
    - Titlul Paginii: {site.page_title}
    - URL: {site.url}
    - Descrierea Produsului/Serviciului: {' '.join(data.paragraphs[:3])}
    - Public Țintă (dacă există): {data.meta_tags.get('target_audience', 'Nespecificat')}
    - Posibilă gamă de preț (dacă există): {data.meta_tags.get('price_range', 'Nespecificat')}
    - Titluri principale de pe pagină (H1, H2): {', '.join(list(data.headings.values())[:5])}
    """

    prompt = f"""
    Pe baza următoarelor informații extrase de pe un site web, te rog să acționezi ca un expert în marketing și să generezi 4 profiluri detaliate de clienți ("personas").

    Informații despre afacere/produs:
    {scraped_info}

    Pentru fiecare dintre cele 4 personas, definește clar următoarele atribute:
    - Nume complet
    - Vârstă
    - Locație
    - Ocupație
    - Venit anual aproximativ
    - Interese și Hobby-uri
    - Provocări și Nevoi (legate de produsul analizat)
    - Motivații (ce i-ar determina să cumpere)
    - Canale de comunicare preferate (ex: Social Media, Email, Bloguri)

    Returnează rezultatul strict în format JSON, cu o listă de obiecte sub cheia "personas". Fiecare obiect trebuie să conțină atributele de mai sus. Nu adăuga niciun text înainte sau după JSON.
    """

    try:
        import openai
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ești un asistent de marketing specializat în crearea de profiluri de clienți (personas)."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Ensure the response is valid JSON
        personas_data = json.loads(response.choices[0].message.content)

        if "personas" not in personas_data or not isinstance(personas_data["personas"], list):
             raise ValueError("Răspunsul JSON de la AI nu are formatul așteptat.")

        for persona_info in personas_data["personas"]:
            AIPersona.objects.create(
                user=request.user,
                name=persona_info.get("name", "N/A"),
                age=persona_info.get("age", 0),
                location=persona_info.get("location", "N/A"),
                occupation=persona_info.get("occupation", "N/A"),
                income=str(persona_info.get("income", "N/A")),
                details=persona_info  # Store all details in the JSON field
            )
        
        messages.success(request, f'✅ Au fost generate și salvate cu succes {len(personas_data["personas"])} noi personas AI!')
        return redirect('auth_app:personas_list')

    except Exception as e:
        messages.error(request, f'A apărut o eroare la generarea personas: {str(e)}')
        return redirect('auth_app:site_detail', site_id=site_id)


@login_required
def scraping_view(request):
    """
    Handles the site scraping process from a single URL input.
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, 'URL-ul este obligatoriu.')
            return render(request, 'auth_app/scraping.html')

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            if not SCRAPER_AVAILABLE:
                messages.error(request, "Scraper-ul nu este disponibil. Contactează administratorul.")
                return render(request, 'auth_app/scraping.html')

            # Use the correct scraper
            scraper = UniversalSuperScraper()
            scraped_data_dict = scraper.extract_all_data(url)

            if 'error' in scraped_data_dict:
                raise Exception(scraped_data_dict['error'])

            domain = urlparse(url).netloc
            site, created = ScrapedSite.objects.update_or_create(
                user=request.user,
                url=url,
                defaults={
                    'domain': domain,
                    'page_title': scraped_data_dict.get('page_title', 'Titlu indisponibil'),
                    'status': 'completed',
                    'scraped_at': timezone.now()
                }
            )
            
            # The ScrapedData model needs to match the keys from the scraper's dictionary
            # Let's assume the model fields are named correctly.
            ScrapedData.objects.update_or_create(
                scraped_site=site,
                defaults=scraped_data_dict
            )
            
            messages.success(request, f'✅ Site-ul {domain} a fost analizat și salvat cu succes!')
            return redirect('auth_app:site_detail', site_id=site.id)

        except Exception as e:
            domain = urlparse(url).netloc if url else 'URL invalid'
            site, created = ScrapedSite.objects.update_or_create(
                user=request.user, url=url,
                defaults={'domain': domain, 'status': 'failed', 'error_message': str(e)}
            )
            messages.error(request, f'A apărut o eroare la analiza site-ului: {e}')
            return redirect('auth_app:site_detail', site_id=site.id)

    return render(request, 'auth_app/scraping.html')

@login_required
def ai_personas_view(request):
    """
    Displays a form to select a scraped site to generate AI personas for.
    """
    sites = ScrapedSite.objects.filter(user=request.user, status='completed').order_by('-scraped_at')
    
    if not OPENAI_AVAILABLE:
        messages.warning(request, 'Funcționalitatea AI nu este disponibilă. Verifică cheia API OpenAI.')

    context = {
        'sites': sites,
        'openai_available': OPENAI_AVAILABLE
    }
    return render(request, 'auth_app/ai_personas.html', context)

@login_required
def personas_list(request):
    """Lista cu toate persoanele generate de utilizator"""
    personas = AIPersona.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'auth_app/personas_list.html', {'personas': personas})

@login_required
def persona_detail(request, persona_id):
    """Detalii despre o persoană generată"""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    return render(request, 'auth_app/persona_detail.html', {'persona': persona})

@login_required
def delete_persona(request, persona_id):
    """Șterge o persoană generată"""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    if request.method == 'POST':
        persona.delete()
        messages.success(request, f'Persoana {persona.name} a fost ștearsă cu succes!')
        return redirect('auth_app:personas_list')
    return render(request, 'auth_app/delete_persona.html', {'persona': persona})

@login_required
def export_persona(request, persona_id):
    """Exportă datele unei persoane în JSON sau CSV"""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    format_type = request.GET.get('format', 'json')
    
    if format_type == 'json':
        data = {
            'name': persona.name,
            'age': persona.age,
            'location': persona.location,
            'occupation': persona.occupation,
            'income': persona.income,
            'education': persona.education,
            'marital_status': persona.marital_status,
            'interests': persona.interests,
            'problems': persona.problems,
            'motivations': persona.motivations,
            'online_behavior': persona.online_behavior,
            'buying_preferences': persona.buying_preferences,
            'communication_channels': persona.communication_channels,
            'objections': persona.objections,
            'created_at': persona.created_at.isoformat()
        }
        
        response = JsonResponse(data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="{persona.name}_persona.json"'
        return response
    
    messages.error(request, 'Format CSV nu este încă implementat.')
    return redirect('auth_app:persona_detail', persona_id=persona_id)

@login_required
def site_list(request):
    """Lista cu toate site-urile scrapate de utilizator"""
    sites = ScrapedSite.objects.filter(user=request.user)
    return render(request, 'auth_app/site_list.html', {'sites': sites})

@login_required
def site_detail(request, site_id):
    """Detalii despre un site scrapat"""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    try:
        data = site.data
        summary = data.get_summary()
    except ScrapedData.DoesNotExist:
        data = None
        summary = {}
    
    context = {
        'site': site,
        'data': data,
        'summary': summary
    }
    return render(request, 'auth_app/site_detail.html', context)

@login_required
def delete_site(request, site_id):
    """Șterge un site scrapat"""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    if request.method == 'POST':
        site.delete()
        messages.success(request, f'Site-ul {site.domain} a fost șters cu succes!')
        return redirect('auth_app:site_list')
    return render(request, 'auth_app/delete_site.html', {'site': site})

@login_required
def export_site_data(request, site_id):
    """Exportă datele unui site în JSON sau CSV"""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    format_type = request.GET.get('format', 'json')
    
    try:
        data = site.data
        if format_type == 'json':
            export_data = {
                'site_info': {
                    'url': site.url,
                    'domain': site.domain,
                    'status': site.status,
                    'page_title': site.page_title,
                    'scraped_at': site.scraped_at.isoformat()
                },
                'scraped_data': {
                    'meta_tags': data.meta_tags,
                    'company_info': data.company_info,
                    'headings': data.headings,
                    'paragraphs': data.paragraphs,
                    'links': data.links,
                    'images': data.images,
                    'contact_info': data.contact_info,
                    'social_media': data.social_media,
                    'statistics': data.statistics
                }
            }
            
            response = JsonResponse(export_data, json_dumps_params={'indent': 2})
            response['Content-Disposition'] = f'attachment; filename="{site.domain}_data.json"'
            return response
        
        elif format_type == 'csv':
            messages.error(request, 'Format CSV nu este încă implementat.')
            return redirect('auth_app:site_detail', site_id=site_id)
            
    except ScrapedData.DoesNotExist:
        messages.error(request, 'Nu există date pentru acest site.')
        return redirect('auth_app:site_detail', site_id=site_id)

@ensure_csrf_cookie
def debug_csrf(request):
    """Debug view to check CSRF token status"""
    context = {
        'csrf_token': request.META.get('CSRF_COOKIE', 'Not found'),
        'session_id': request.session.session_key,
        'cookies': dict(request.COOKIES),
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
        'method': request.method,
    }
    return render(request, 'auth_app/debug_csrf.html', context)
