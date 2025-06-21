#!/usr/bin/env python3
"""
Script de test pentru funcționalitatea de scraping
"""

import os
import sys
import django

# Adaugă calea către proiectul Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurează Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

from auth_app.models import ScrapedSite, ScrapedData
from auth_app.views import scraping_view
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

def test_scraping_functionality():
    """Testează funcționalitatea de scraping"""
    print("🧪 Testare funcționalitate scraping...")
    
    # Verifică dacă există utilizatori
    users = User.objects.all()
    if not users.exists():
        print("❌ Nu există utilizatori în baza de date")
        return False
    
    user = users.first()
    print(f"✅ Utilizator găsit: {user.username}")
    
    # Verifică site-urile existente
    sites = ScrapedSite.objects.filter(user=user)
    print(f"📊 Site-uri existente: {sites.count()}")
    
    for site in sites:
        print(f"   - {site.domain} ({site.status}) - {site.scraped_at}")
        try:
            data = site.data
            print(f"     📄 Date: {len(data.paragraphs)} paragrafe, {len(data.links)} linkuri")
        except ScrapedData.DoesNotExist:
            print(f"     ❌ Fără date")
    
    # Testează importul scraper-ului
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper_test'))
        from universal_super_scraper import UniversalSuperScraper
        print("✅ Scraper importat cu succes")
        
        # Testează scraping-ul pe un site simplu
        scraper = UniversalSuperScraper()
        test_url = "https://httpbin.org/html"
        print(f"🔍 Testare scraping pe {test_url}...")
        
        data = scraper.extract_all_data(test_url)
        
        if 'error' not in data:
            print("✅ Scraping test reușit!")
            print(f"   - Titlu: {data.get('page_title', 'N/A')}")
            print(f"   - Paragrafe: {len(data.get('paragraphs', []))}")
            print(f"   - Linkuri: {len(data.get('links', []))}")
            print(f"   - Imagini: {len(data.get('images', []))}")
            
            # Testează salvarea în baza de date
            print("💾 Testare salvare în baza de date...")
            
            # Creează site-ul
            site = ScrapedSite.objects.create(
                user=user,
                url=test_url,
                domain="httpbin.org",
                status='completed',
                page_title=data.get('page_title', '')
            )
            
            # Salvează datele
            scraped_data = ScrapedData.objects.create(
                scraped_site=site,
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
            
            print("✅ Date salvate cu succes în baza de date!")
            print(f"   - Site ID: {site.id}")
            print(f"   - Data ID: {scraped_data.id}")
            
            # Testează accesarea datelor
            retrieved_data = site.data
            print(f"✅ Date accesate cu succes: {len(retrieved_data.paragraphs)} paragrafe")
            
            return True
            
        else:
            print(f"❌ Eroare la scraping: {data['error']}")
            return False
            
    except ImportError as e:
        print(f"❌ Eroare la importul scraper-ului: {e}")
        return False
    except Exception as e:
        print(f"❌ Eroare neașteptată: {e}")
        return False

def test_export_functionality():
    """Testează funcționalitatea de export"""
    print("\n📤 Testare funcționalitate export...")
    
    sites = ScrapedSite.objects.filter(status='completed')
    if not sites.exists():
        print("❌ Nu există site-uri completate pentru test")
        return False
    
    site = sites.first()
    print(f"✅ Testare export pentru site: {site.domain}")
    
    try:
        # Testează exportul JSON
        from auth_app.views import export_site_data
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get(f'/sites/{site.id}/export/?format=json')
        
        # Adaugă middleware pentru sesiuni și autentificare
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        auth_middleware = AuthenticationMiddleware(lambda x: None)
        auth_middleware.process_request(request)
        
        # Setează utilizatorul
        request.user = site.user
        
        # Adaugă storage pentru mesaje
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = export_site_data(request, site.id)
        
        if response.status_code == 200:
            print("✅ Export JSON funcționează!")
            print(f"   - Content-Type: {response.get('Content-Type', 'N/A')}")
            print(f"   - Content-Disposition: {response.get('Content-Disposition', 'N/A')}")
        else:
            print(f"❌ Eroare la export JSON: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Eroare la testarea export-ului: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Începe testarea funcționalității de scraping...")
    
    success = True
    
    # Testează scraping-ul
    if not test_scraping_functionality():
        success = False
    
    # Testează export-ul
    if not test_export_functionality():
        success = False
    
    if success:
        print("\n🎉 Toate testele au trecut cu succes!")
        print("✅ Aplicația este gata pentru utilizare")
    else:
        print("\n❌ Unele teste au eșuat")
        print("⚠️  Verifică configurația și încercă din nou") 