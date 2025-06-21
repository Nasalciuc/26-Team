from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from urllib.parse import urlparse
import sys
import os
import json
from datetime import datetime

# Import scraper-ul
try:
    # This complex path logic is necessary to handle both local dev and Docker environments
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_path = os.path.join(current_dir, '..', 'scripts')
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    from NOD1 import UniversalSuperScraper
    SCRAPER_AVAILABLE = True
    print("✅ Scraper imported successfully.")
except ImportError as e:
    SCRAPER_AVAILABLE = False
    print(f"Scraper Import Warning: {e}")


from .models import ScrapedSite, ScrapedData, AIPersona
from .forms import ScrapingForm

# OpenAI Configuration
try:
    import openai
    # Load the API key from an environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        OPENAI_AVAILABLE = False
        print("Warning: OPENAI_API_KEY environment variable not set. AI Personas functionality will be limited.")
    else:
        OPENAI_AVAILABLE = True
        print("✅ OpenAI API key configured successfully.")
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not installed. AI Personas functionality will be limited.")
except Exception as e:
    OPENAI_AVAILABLE = False
    print(f"Warning: Could not configure OpenAI. Error: {e}")

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
    recent_sites = ScrapedSite.objects.filter(user=request.user).order_by('-scraped_at')[:5]
    recent_personas = AIPersona.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_sites': recent_sites,
        'recent_personas': recent_personas,
        'total_sites': ScrapedSite.objects.filter(user=request.user).count(),
        'total_personas': AIPersona.objects.filter(user=request.user).count(),
        'scraper_available': SCRAPER_AVAILABLE,
        'openai_available': OPENAI_AVAILABLE,
    }
    return render(request, 'auth_app/dashboard.html', context)


@login_required
def generate_personas_from_site(request, site_id):
    """
    Generates AI personas based on the scraped data of a specific site.
    """
    if request.method != 'POST':
        messages.error(request, "Metodă invalidă.")
        return redirect('auth_app:ai_personas')

    if not OPENAI_AVAILABLE:
        messages.error(request, 'Funcționalitatea AI nu este disponibilă. Verifică cheia API OpenAI.')
        return redirect('auth_app:ai_personas')

    try:
        site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
        # Access the related ScrapedData object. Using 'data' as related_name.
        data = site.data
    except ScrapedData.DoesNotExist:
        messages.error(request, 'Datele pentru acest site nu au fost găsite. Rulați din nou analiza.')
        return redirect('auth_app:site_detail', site_id=site_id)
    except Exception as e:
        messages.error(request, f"A apărut o eroare la preluarea datelor site-ului: {e}")
        return redirect('auth_app:ai_personas')

    prompt_parts = [
        "Analizează următoarele date extrase de pe un site web și generează 5 profiluri de client (personas) distincte și detaliate. Fiecare profil trebuie să fie în format JSON și să includă: nume, vârstă, ocupație, nevoi, frustrări, și un scurt scenariu de utilizare a site-ului. Prezintă toate cele 5 profiluri într-un singur array JSON numit 'personas'. Datele site-ului sunt:",
        f"- URL: {site.url}",
        f"- Titlul paginii: {getattr(data, 'page_title', 'N/A')}",
        f"- Meta Descriere: {getattr(data, 'meta_tags', {}).get('description', 'N/A')}",
    ]

    # Flatten the list of lists of headings into a single list of strings
    all_headings = []
    headings_dict = getattr(data, 'headings', {})
    if isinstance(headings_dict, dict):
        for heading_list in headings_dict.values():
            if isinstance(heading_list, list):
                # Ensure all items in the list are strings before extending
                all_headings.extend([str(item) for item in heading_list])

    if all_headings:
        prompt_parts.append(f"- Titluri principale (H1, H2, etc.): {', '.join(all_headings[:10])}")

    paragraphs = getattr(data, 'paragraphs', [])
    if paragraphs and isinstance(paragraphs, list):
        prompt_parts.append(f"- Primele paragrafe: {' '.join(paragraphs[:3])}")
    
    links = getattr(data, 'links', [])
    if links and isinstance(links, list):
        link_texts = [link.get('text', '') for link in links if link.get('text')]
        if link_texts:
            prompt_parts.append(f"- Text ancore linkuri: {', '.join(link_texts[:10])}")

    prompt = "\n".join(prompt_parts)

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ești un asistent de marketing specializat în crearea de profiluri de clienți (personas). Răspunsul tău trebuie să fie un obiect JSON valid care conține un singur array, numit 'personas'."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        response_content = response.choices[0].message.content
        personas_data = json.loads(response_content)

        if "personas" not in personas_data or not isinstance(personas_data["personas"], list):
             raise ValueError("Răspunsul JSON de la AI nu are formatul așteptat (lipsește array-ul 'personas').")

        # Delete existing personas for this site to avoid duplicates
        AIPersona.objects.filter(user=request.user, source_site=site).delete()

        for persona_info in personas_data["personas"]:
            AIPersona.objects.create(
                user=request.user,
                source_site=site,
                name=persona_info.get("nume", "N/A"),
                age=persona_info.get("vârstă", 0),
                occupation=persona_info.get("ocupație", "N/A"),
                details=persona_info
            )
        
        messages.success(request, f'✅ Au fost generate și salvate cu succes {len(personas_data["personas"])} noi profiluri AI pentru {site.domain}!')
        return redirect('auth_app:personas_list')

    except json.JSONDecodeError:
        messages.error(request, f"Eroare: AI-ul a returnat un răspuns invalid (nu este JSON). Răspuns primit: {response_content}")
        return redirect('auth_app:site_detail', site_id=site_id)
    except Exception as e:
        messages.error(request, f'A apărut o eroare la generarea profilurilor: {str(e)}')
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
            
            ScrapedData.objects.update_or_create(
                site=site,
                defaults={'data': scraped_data_dict}
            )
            
            messages.success(request, f"Site-ul {url} a fost analizat cu succes!")
            return redirect('auth_app:site_detail', site_id=site.id)

        except Exception as e:
            messages.error(request, f"A apărut o eroare la analizarea site-ului: {str(e)}")
            return render(request, 'auth_app/scraping.html')

    return render(request, 'auth_app/scraping.html')


@login_required
def ai_personas_view(request):
    """
    Displays the list of sites to choose from for generating AI personas.
    """
    sites = ScrapedSite.objects.filter(user=request.user, status='completed').order_by('-scraped_at')
    context = {
        'sites': sites,
        'openai_available': OPENAI_AVAILABLE,
    }
    return render(request, 'auth_app/ai_personas.html', context)

@login_required
def personas_list(request):
    """Displays the list of generated AI personas."""
    personas = AIPersona.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'auth_app/personas_list.html', {'personas': personas})

@login_required
def persona_detail(request, persona_id):
    """Displays details of a single AI persona."""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    return render(request, 'auth_app/persona_detail.html', {'persona': persona})

@login_required
def delete_persona(request, persona_id):
    """Deletes an AI persona."""
    if request.method == 'POST':
        persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
        persona.delete()
        messages.success(request, 'Profilul AI a fost șters cu succes.')
        return redirect('auth_app:personas_list')
    else:
        # If not POST, redirect to the list
        return redirect('auth_app:personas_list')

@login_required
def export_persona(request, persona_id):
    """Exports a single persona as a JSON file."""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    
    # Prepare the data for export
    export_data = {
        "name": persona.name,
        "age": persona.age,
        "occupation": persona.occupation,
        "details": persona.details,
        "source_site": persona.source_site.url if persona.source_site else "N/A",
        "created_at": persona.created_at.isoformat(),
    }
    
    response = HttpResponse(
        json.dumps(export_data, indent=4, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
    filename = f"persona_{persona.name.replace(' ', '_')}_{persona.id}.json"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def site_list(request):
    """Displays the list of scraped sites."""
    sites = ScrapedSite.objects.filter(user=request.user).order_by('-scraped_at')
    return render(request, 'auth_app/site_list.html', {'sites': sites})

@login_required
def site_detail(request, site_id):
    """Displays details and data of a scraped site."""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    try:
        scraped_data = site.data.data  # Access the JSONField 'data' on the ScrapedData instance
    except ScrapedData.DoesNotExist:
        scraped_data = None
        messages.warning(request, "Nu s-au găsit date detaliate pentru acest site.")
    
    context = {
        'site': site,
        'scraped_data': scraped_data,
        'openai_available': OPENAI_AVAILABLE
    }
    return render(request, 'auth_app/site_detail.html', context)


@login_required
def delete_site(request, site_id):
    """Deletes a scraped site and all related data."""
    if request.method == 'POST':
        site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
        site_url = site.url
        site.delete()
        messages.success(request, f'Site-ul {site_url} și datele asociate au fost șterse.')
        return redirect('auth_app:site_list')
    return redirect('auth_app:site_list')


@login_required
def export_site_data(request, site_id):
    """Exports the scraped data of a site as a JSON file."""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    try:
        data_to_export = site.data.data
        
        # Function to convert datetime objects to string
        def default(o):
            if isinstance(o, (datetime)):
                return o.isoformat()

        json_data = json.dumps(data_to_export, indent=4, ensure_ascii=False, default=default)
        
        response = HttpResponse(json_data, content_type='application/json; charset=utf-8')
        filename = f"scraped_data_{site.domain}_{site.id}.json"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except ScrapedData.DoesNotExist:
        messages.error(request, "Nu s-au găsit date de exportat pentru acest site.")
        return redirect('auth_app:site_detail', site_id=site_id)
    except Exception as e:
        messages.error(request, f"A apărut o eroare la export: {e}")
        return redirect('auth_app:site_detail', site_id=site_id)

@ensure_csrf_cookie
def debug_csrf(request):
    """A simple view to help debug CSRF issues."""
    return render(request, 'auth_app/debug_csrf.html')
