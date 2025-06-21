from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from urllib.parse import urlparse
import sys
import os
import json
from datetime import datetime

# Import scraper-ul
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper_test'))
    from universal_super_scraper import UniversalSuperScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    print("Warning: DrissionPage not available. Scraping functionality will be limited.")

from .models import ScrapedSite, ScrapedData
from .forms import ScrapingForm

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
    # Obține ultimele 5 site-uri scrapate de utilizator
    recent_sites = ScrapedSite.objects.filter(user=request.user)[:5]
    
    context = {
        'recent_sites': recent_sites,
        'total_sites': ScrapedSite.objects.filter(user=request.user).count(),
        'completed_sites': ScrapedSite.objects.filter(user=request.user, status='completed').count(),
        'scraper_available': SCRAPER_AVAILABLE,
    }
    return render(request, 'auth_app/dashboard.html', context)

@login_required
def scraping_view(request):
    """View pentru introducerea URL-ului și inițierea scraping-ului"""
    if not SCRAPER_AVAILABLE:
        messages.warning(request, 'Scraper-ul nu este disponibil. Vă rugăm să instalați DrissionPage pentru funcționalitate completă.')
        return render(request, 'auth_app/scraping.html', {'form': None, 'scraper_available': False})
    
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            domain = urlparse(url).netloc
            
            # Verifică dacă site-ul a fost deja scrapat recent de acest utilizator
            existing_site = ScrapedSite.objects.filter(
                user=request.user, 
                url=url, 
                scraped_at__gte=timezone.now() - timezone.timedelta(hours=1)
            ).first()
            
            if existing_site:
                messages.info(request, f'Site-ul {domain} a fost deja analizat recent. Vezi rezultatele în lista de site-uri.')
                return redirect('auth_app:site_detail', site_id=existing_site.id)
            
            # Creează înregistrarea în baza de date
            scraped_site = ScrapedSite.objects.create(
                user=request.user,
                url=url,
                domain=domain,
                status='processing'
            )
            
            # Inițiază scraping-ul
            try:
                scraper = UniversalSuperScraper()
                data = scraper.extract_all_data(url)
                
                if 'error' not in data:
                    # Salvează datele în baza de date
                    scraped_data = ScrapedData.objects.create(
                        scraped_site=scraped_site,
                        meta_tags=data.get('meta_tags', {}),
                        company_info=data.get('company_info', {}),
                        headings=data.get('headings', {}),
                        paragraphs=data.get('paragraphs', []),
                        links=data.get('links', []),
                        images=data.get('images', []),
                        buttons=data.get('buttons', []),
                        forms=data.get('forms', []),
                        lists=data.get('lists', []),
                        tables=data.get('tables', []),
                        scripts=data.get('scripts', []),
                        styles=data.get('styles', []),
                        contact_info=data.get('contact_info', {}),
                        social_media=data.get('social_media', {}),
                        statistics=data.get('statistics', []),
                        css_classes=data.get('css_classes', []),
                        element_ids=data.get('element_ids', []),
                        important_divs=data.get('important_divs', []),
                        important_spans=data.get('important_spans', [])
                    )
                    
                    # Actualizează statusul
                    scraped_site.status = 'completed'
                    scraped_site.page_title = data.get('page_title', '')
                    scraped_site.save()
                    
                    # Mesaj de succes cu statistici
                    total_links = len(data.get('links', []))
                    total_images = len(data.get('images', []))
                    total_paragraphs = len(data.get('paragraphs', []))
                    
                    messages.success(request, 
                        f'✅ Scraping completat cu succes pentru {domain}! '
                        f'Găsite: {total_links} linkuri, {total_images} imagini, {total_paragraphs} paragrafe.'
                    )
                    return redirect('auth_app:site_detail', site_id=scraped_site.id)
                else:
                    scraped_site.status = 'failed'
                    scraped_site.error_message = data['error']
                    scraped_site.save()
                    messages.error(request, f'❌ Eroare la scraping: {data["error"]}')
                    
            except Exception as e:
                scraped_site.status = 'failed'
                scraped_site.error_message = str(e)
                scraped_site.save()
                messages.error(request, f'❌ Eroare la scraping: {str(e)}')
    else:
        form = ScrapingForm()
    
    context = {
        'form': form,
        'scraper_available': SCRAPER_AVAILABLE,
        'recent_sites': ScrapedSite.objects.filter(user=request.user)[:5]
    }
    return render(request, 'auth_app/scraping.html', context)

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
    """Exportă datele unui site în format JSON sau CSV"""
    site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    format_type = request.GET.get('format', 'json')
    
    try:
        data = site.data
        export_data = {
            'url': site.url,
            'domain': site.domain,
            'scraped_at': site.scraped_at.isoformat(),
            'page_title': site.page_title,
            'meta_tags': data.meta_tags,
            'company_info': data.company_info,
            'headings': data.headings,
            'paragraphs': data.paragraphs,
            'links': data.links,
            'images': data.images,
            'buttons': data.buttons,
            'forms': data.forms,
            'lists': data.lists,
            'tables': data.tables,
            'scripts': data.scripts,
            'styles': data.styles,
            'contact_info': data.contact_info,
            'social_media': data.social_media,
            'statistics': data.statistics,
            'css_classes': data.css_classes,
            'element_ids': data.element_ids,
            'important_divs': data.important_divs,
            'important_spans': data.important_spans,
        }
        
        if format_type == 'json':
            response = JsonResponse(export_data, json_dumps_params={'indent': 2})
            response['Content-Disposition'] = f'attachment; filename="{site.domain}_{site.scraped_at.strftime("%Y%m%d_%H%M%S")}.json"'
            return response
        else:
            # CSV export
            import csv
            from django.http import HttpResponse
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{site.domain}_{site.scraped_at.strftime("%Y%m%d_%H%M%S")}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Tip Informație', 'Conținut', 'URL', 'Data Scraping'])
            
            if site.page_title:
                writer.writerow(['Titlu Pagină', site.page_title, site.url, site.scraped_at])
            
            for heading_type, headings in data.headings.items():
                for heading in headings:
                    writer.writerow([f'Heading {heading_type.upper()}', heading, site.url, site.scraped_at])
            
            for paragraph in data.paragraphs:
                writer.writerow(['Paragraf', paragraph, site.url, site.scraped_at])
            
            for link in data.links:
                writer.writerow(['Link', f"{link['text']} - {link['url']}", site.url, site.scraped_at])
            
            for img in data.images:
                writer.writerow(['Imagine', f"{img['alt']} - {img['src']}", site.url, site.scraped_at])
            
            return response
            
    except ScrapedData.DoesNotExist:
        messages.error(request, 'Nu există date pentru acest site.')
        return redirect('auth_app:site_detail', site_id=site_id)
