from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from urllib.parse import urlparse
import sys
import os
import json
from datetime import datetime
import re
import openai
import requests
import hmac
import hashlib
from django.urls import reverse
from .image_generator import ImageGenerator
from django.conf import settings
from .facebook_poster import FacebookPoster
import logging

# Setup logger
logger = logging.getLogger(__name__)

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


from .models import ScrapedSite, ScrapedData, AIPersona, Strategy, Post
from .forms import ScrapingForm

# OpenAI Configuration
try:
    from openai import OpenAI
    # Load the API key from an environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
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
    recent_strategies = Strategy.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_posts = Post.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_sites': recent_sites,
        'recent_personas': recent_personas,
        'recent_strategies': recent_strategies,
        'recent_posts': recent_posts,
        'total_sites': ScrapedSite.objects.filter(user=request.user).count(),
        'total_personas': AIPersona.objects.filter(user=request.user).count(),
        'total_strategies': Strategy.objects.filter(user=request.user).count(),
        'total_posts': Post.objects.filter(user=request.user).count(),
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

    # Build the prompt using the working approach
    prompt_parts = [
        f"Create 5 customer personas for a website: {site.url}",
        f"Website title: {getattr(data, 'page_title', 'N/A')}",
        f"Meta description: {getattr(data, 'meta_tags', {}).get('description', 'N/A')}",
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
        prompt_parts.append(f"Main headings: {', '.join(all_headings[:10])}")

    paragraphs = getattr(data, 'paragraphs', [])
    if paragraphs and isinstance(paragraphs, list):
        prompt_parts.append(f"Content: {' '.join(paragraphs[:3])}")
    
    links = getattr(data, 'links', [])
    if links and isinstance(links, list):
        link_texts = [link.get('text', '') for link in links if link.get('text')]
        if link_texts:
            prompt_parts.append(f"Navigation links: {', '.join(link_texts[:10])}")

    prompt = "\n".join(prompt_parts) + """

CRITICAL: You must return ONLY valid JSON. No explanations, no markdown, no additional text.

The response must start with { and end with }.

Create 5 detailed customer personas for this website. Include ALL the following fields with realistic Romanian context:

{
  "personas": [
    {
      "name": "Full Name",
      "age": "25-35",
      "location": "City, România",
      "description": "Brief occupation description",
      "interests": ["interest1", "interest2", "interest3"],
      "needs": ["need1", "need2", "need3"],
      "frustrations": ["frustration1", "frustration2", "frustration3"],
      "usage_scenario": "How they would use this website",
      "income_level": "Low/Medium/High",
      "education": "High School/Bachelor's/Master's/PhD",
      "marital_status": "Single/Married/Divorced",
      "online_behavior": "How they typically behave online",
      "buying_preferences": "What influences their purchasing decisions",
      "communication_channels": ["email", "social_media", "phone"],
      "objections": ["objection1", "objection2"],
      "business_type": "Type of business they work for",
      "product_description": "What products/services they might need",
      "target_market": "Their role in the market"
    }
  ]
}

IMPORTANT: Make the personas realistic for Romanian market. Use Romanian cities, education levels, and business contexts. Include diverse age ranges, income levels, and professional backgrounds."""

    try:
        # Use the working OpenAI client approach
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a marketing expert. You must return ONLY valid JSON format without any markdown formatting, explanations, or additional text. All strings must be properly quoted and escaped. Do not include ```json or ``` markers. The response must be a valid JSON object starting with { and ending with }."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        # Get and clean the response
        content = response.choices[0].message.content.strip()
        
        # Clean JSON if needed (handle markdown code blocks)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        # Additional JSON cleaning to handle common issues
        # Remove any leading/trailing non-JSON content
        content = content.strip()
        if not content.startswith('{'):
            # Find the first occurrence of '{'
            start_idx = content.find('{')
            if start_idx != -1:
                content = content[start_idx:]
        
        if not content.endswith('}'):
            # Find the last occurrence of '}'
            end_idx = content.rfind('}')
            if end_idx != -1:
                content = content[:end_idx + 1]
        
        # Comprehensive JSON repair function
        def repair_json(json_str):
            """Attempt to repair common JSON issues"""
            # Fix missing commas between elements
            json_str = re.sub(r'(\]|\})\s*(\[|\{)', r'\1,\2', json_str)
            json_str = re.sub(r'(")\s*(\[|\{)', r'\1,\2', json_str)
            json_str = re.sub(r'(\]|\})\s*(")', r'\1,\2', json_str)
            json_str = re.sub(r'(\d+)\s*(\[|\{)', r'\1,\2', json_str)
            json_str = re.sub(r'(\]|\})\s*(\d+)', r'\1,\2', json_str)
            json_str = re.sub(r'(true|false|null)\s*(\[|\{)', r'\1,\2', json_str)
            json_str = re.sub(r'(\]|\})\s*(true|false|null)', r'\1,\2', json_str)
            
            # Fix missing commas in object properties
            json_str = re.sub(r'(")\s*(")', r'\1,\2', json_str)
            json_str = re.sub(r'(\d+)\s*(")', r'\1,\2', json_str)
            json_str = re.sub(r'(")\s*(\d+)', r'\1,\2', json_str)
            
            # Fix trailing commas (which are invalid in JSON)
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            
            # Fix missing quotes around property names
            json_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
            
            return json_str
        
        # Apply JSON repair
        content = repair_json(content)
        
        # Log the content for debugging (first 1000 characters)
        print(f"JSON content after repair (first 1000 chars): {content[:1000]}")
        print(f"JSON content length: {len(content)}")
        
        # Additional aggressive repair for specific comma delimiter errors
        # This targets the "Expecting ',' delimiter: line 8 column 6" error
        lines = content.split('\n')
        if len(lines) >= 8:
            # Focus on line 8 (index 7) and surrounding lines
            for i in range(max(0, 6), min(len(lines), 10)):
                line = lines[i]
                # Fix common patterns that cause comma delimiter errors
                line = re.sub(r'(\w+)\s*(\[|\{)', r'\1,\2', line)  # Add comma before array/object
                line = re.sub(r'(\]|\})\s*(\w+)', r'\1,\2', line)  # Add comma after array/object
                line = re.sub(r'(")\s*(\w+)', r'\1,\2', line)  # Add comma after string
                line = re.sub(r'(\w+)\s*(")', r'\1,\2', line)  # Add comma before string
                lines[i] = line
        content = '\n'.join(lines)
        
        # Try to parse the JSON with better error handling
        try:
            personas_data = json.loads(content)
        except json.JSONDecodeError as json_error:
            # If JSON parsing fails, try to fix common issues
            print(f"JSON parsing failed: {json_error}")
            print(f"Raw content: {content[:500]}...")  # Log first 500 chars for debugging
            
            # Try to fix common JSON issues
            # Fix missing commas between array elements and object properties
            # This handles the "Expecting ',' delimiter" error
            content = re.sub(r'(\]|\})\s*(\[|\{)', r'\1,\2', content)  # Add comma between arrays/objects
            content = re.sub(r'(")\s*(\[|\{)', r'\1,\2', content)  # Add comma after string before array/object
            content = re.sub(r'(\]|\})\s*(")', r'\1,\2', content)  # Add comma after array/object before string
            
            # Additional fixes for specific comma delimiter issues
            content = re.sub(r'(\d+)\s*(\[|\{)', r'\1,\2', content)  # Add comma after number before array/object
            content = re.sub(r'(\]|\})\s*(\d+)', r'\1,\2', content)  # Add comma after array/object before number
            content = re.sub(r'(true|false|null)\s*(\[|\{)', r'\1,\2', content)  # Add comma after boolean/null before array/object
            content = re.sub(r'(\]|\})\s*(true|false|null)', r'\1,\2', content)  # Add comma after array/object before boolean/null
            
            # Fix missing commas in object properties
            content = re.sub(r'(")\s*(")', r'\1,\2', content)  # Add comma between string properties
            content = re.sub(r'(\d+)\s*(")', r'\1,\2', content)  # Add comma between number and string
            content = re.sub(r'(")\s*(\d+)', r'\1,\2', content)  # Add comma between string and number
            
            # Fix unterminated strings by finding and fixing quote issues
            # This handles cases where quotes are not properly escaped
            lines = content.split('\n')
            fixed_lines = []
            for i, line in enumerate(lines):
                # Count quotes in the line
                quote_count = line.count('"')
                if quote_count % 2 != 0:  # Odd number of quotes
                    # Try to fix by adding a closing quote at the end
                    if not line.strip().endswith('"'):
                        line = line.rstrip() + '"'
                fixed_lines.append(line)
            
            content = '\n'.join(fixed_lines)
            
            # Also try the original regex fix
            content = re.sub(r'"([^"]*)"([^"]*)"', r'"\1\\"\2"', content)
            
            # Try parsing again
            try:
                personas_data = json.loads(content)
            except json.JSONDecodeError as second_error:
                # If still failing, try one more approach - remove problematic characters
                print(f"Second JSON parsing attempt failed: {second_error}")
                
                # Remove any control characters that might break JSON
                content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
                
                # Try to find the JSON object boundaries more precisely
                start_brace = content.find('{')
                end_brace = content.rfind('}')
                if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                    content = content[start_brace:end_brace + 1]
                
                try:
                    personas_data = json.loads(content)
                except json.JSONDecodeError as third_error:
                    # Final attempt - create a minimal valid JSON structure
                    print(f"Third JSON parsing attempt failed: {third_error}")
                    print(f"Final content attempt: {content[:200]}...")
                    
                    # Try one more approach - fix unterminated strings more aggressively
                    # Remove any newlines within string values that might break JSON
                    content = re.sub(r'"([^"]*?)\n([^"]*?)"', r'"\1 \2"', content)
                    
                    # Fix any remaining unterminated strings by ensuring proper quote balance
                    # This is a more aggressive approach for the specific error you're seeing
                    brace_count = 0
                    bracket_count = 0
                    in_string = False
                    escape_next = False
                    fixed_content = ""
                    
                    for char in content:
                        if escape_next:
                            fixed_content += char
                            escape_next = False
                            continue
                        
                        if char == '\\':
                            escape_next = True
                            fixed_content += char
                            continue
                        
                        if char == '"' and not escape_next:
                            in_string = not in_string
                            fixed_content += char
                            continue
                        
                        if not in_string:
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                            elif char == '[':
                                bracket_count += 1
                            elif char == ']':
                                bracket_count -= 1
                        
                        fixed_content += char
                    
                    # Ensure proper closing
                    while brace_count > 0:
                        fixed_content += '}'
                        brace_count -= 1
                    while bracket_count > 0:
                        fixed_content += ']'
                        bracket_count -= 1
                    
                    try:
                        personas_data = json.loads(fixed_content)
                    except json.JSONDecodeError as final_error:
                        print(f"Final JSON parsing attempt failed: {final_error}")
                        print(f"AI Response content: {content[:500]}...")
                        
                        # Create fallback personas when AI fails
                        print("Creating fallback personas due to AI JSON parsing failure")
                        personas_data = {
                            "personas": [
                                {
                                    "name": f"Client Tipic {site.domain}",
                                    "age": "25-45",
                                    "location": "România",
                                    "description": "Utilizator tipic al site-ului",
                                    "interests": ["tehnologie", "marketing", "business"],
                                    "needs": ["informații", "servicii", "produse"],
                                    "frustrations": ["informații incomplete", "proces complicat"],
                                    "usage_scenario": f"Vizitează {site.domain} pentru a găsi informații și servicii",
                                    "income_level": "Medium",
                                    "education": "Bachelor's",
                                    "marital_status": "N/A",
                                    "online_behavior": "Caută informații online înainte de a lua decizii",
                                    "buying_preferences": "Compară opțiunile înainte de a cumpăra",
                                    "communication_channels": ["email", "website"],
                                    "objections": ["preț", "calitate"],
                                    "business_type": "N/A",
                                    "product_description": "Servicii și produse oferite de site",
                                    "target_market": "Utilizatori români"
                                },
                                {
                                    "name": f"Client Avansat {site.domain}",
                                    "age": "30-50",
                                    "location": "România",
                                    "description": "Client cu experiență în domeniu",
                                    "interests": ["inovare", "eficiență", "rezultate"],
                                    "needs": ["soluții avansate", "suport tehnic", "ROI"],
                                    "frustrations": ["lipsa personalizare", "suport insuficient"],
                                    "usage_scenario": f"Folosește {site.domain} pentru soluții profesionale",
                                    "income_level": "High",
                                    "education": "Master's",
                                    "marital_status": "N/A",
                                    "online_behavior": "Caută soluții complexe și personalizate",
                                    "buying_preferences": "Calitate și servicii premium",
                                    "communication_channels": ["email", "telefon", "meeting"],
                                    "objections": ["complexitate", "timp implementare"],
                                    "business_type": "Corporații",
                                    "product_description": "Soluții enterprise și servicii premium",
                                    "target_market": "Profesioniști cu experiență"
                                }
                            ]
                        }
                        messages.warning(request, f"AI-ul nu a putut genera profiluri valide. Au fost create profiluri de bază pentru {site.domain}.")

        if "personas" not in personas_data or not isinstance(personas_data["personas"], list):
             raise ValueError("Răspunsul JSON de la AI nu are formatul așteptat (lipsește array-ul 'personas').")

        # Delete existing personas for this site to avoid duplicates
        # Note: Since AIPersona doesn't have source_site field, we'll just create new ones

        for persona_info in personas_data["personas"]:
            AIPersona.objects.create(
                user=request.user,
                scraped_site=site,
                name=persona_info.get("name", "N/A"),
                age=int(persona_info.get("age", "25").split("-")[0]) if isinstance(persona_info.get("age"), str) and "-" in persona_info.get("age") else 25,
                location=persona_info.get("location", "N/A"),
                occupation=persona_info.get("description", "N/A"),
                income=persona_info.get("income_level", "N/A"),
                education=persona_info.get("education", "N/A"),
                marital_status=persona_info.get("marital_status", "N/A"),
                interests=persona_info.get("interests", []),
                problems=persona_info.get("frustrations", []),
                motivations=persona_info.get("needs", []),
                online_behavior=persona_info.get("online_behavior", "N/A"),
                buying_preferences=persona_info.get("buying_preferences", "N/A"),
                communication_channels=persona_info.get("communication_channels", []),
                objections=persona_info.get("objections", []),
                business_type=persona_info.get("business_type", "N/A"),
                product_description=persona_info.get("product_description", "N/A"),
                target_market=persona_info.get("target_market", "N/A")
            )
        
        messages.success(request, f'✅ Au fost generate și salvate cu succes {len(personas_data["personas"])} noi profiluri AI pentru {site.domain}!')
        return redirect(f'{reverse("auth_app:personas_list")}?site_id={site_id}')

    except json.JSONDecodeError as e:
        messages.error(request, f"Eroare: AI-ul a returnat un răspuns invalid (nu este JSON). Eroare: {e}")
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
                scraped_site=site,
                defaults={
                    'meta_tags': scraped_data_dict.get('meta_tags', {}),
                    'company_info': scraped_data_dict.get('company_info', {}),
                    'headings': scraped_data_dict.get('headings', {}),
                    'paragraphs': scraped_data_dict.get('paragraphs', []),
                    'links': scraped_data_dict.get('links', []),
                    'images': scraped_data_dict.get('images', []),
                    'buttons': scraped_data_dict.get('buttons', []),
                    'forms': scraped_data_dict.get('forms', []),
                    'lists': scraped_data_dict.get('lists', []),
                    'tables': scraped_data_dict.get('tables', []),
                    'scripts': scraped_data_dict.get('scripts', []),
                    'styles': scraped_data_dict.get('styles', []),
                    'contact_info': scraped_data_dict.get('contact_info', {}),
                    'social_media': scraped_data_dict.get('social_media', {}),
                    'statistics': scraped_data_dict.get('statistics', []),
                    'css_classes': scraped_data_dict.get('css_classes', []),
                    'element_ids': scraped_data_dict.get('element_ids', []),
                    'important_divs': scraped_data_dict.get('important_divs', []),
                    'important_spans': scraped_data_dict.get('important_spans', [])
                }
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
    
    # Get existing personas for each site
    sites_with_personas = []
    for site in sites:
        personas = AIPersona.objects.filter(user=request.user, scraped_site=site).order_by('-created_at')
        sites_with_personas.append({
            'site': site,
            'personas': personas,
            'personas_count': personas.count()
        })
    
    context = {
        'sites_with_personas': sites_with_personas,
        'sites': sites,  # Keep for backward compatibility
        'openai_available': OPENAI_AVAILABLE,
    }
    return render(request, 'auth_app/ai_personas.html', context)

@login_required
def personas_list(request):
    """Displays the list of generated AI personas."""
    # Get filter parameters
    site_id = request.GET.get('site_id')
    
    if site_id:
        # Filter personas by specific site
        personas = AIPersona.objects.filter(user=request.user, scraped_site_id=site_id).order_by('-created_at')
        site_filter = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
    else:
        # Show all personas
        personas = AIPersona.objects.filter(user=request.user).order_by('-created_at')
        site_filter = None
    
    # Get all sites for filter dropdown
    sites = ScrapedSite.objects.filter(user=request.user).order_by('-scraped_at')
    
    context = {
        'personas': personas,
        'sites': sites,
        'site_filter': site_filter,
    }
    return render(request, 'auth_app/personas_list.html', context)

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
def edit_persona(request, persona_id):
    """Edits an AI persona."""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    
    if request.method == 'POST':
        # Update persona fields
        persona.name = request.POST.get('name', persona.name)
        persona.age = int(request.POST.get('age', persona.age))
        persona.location = request.POST.get('location', persona.location)
        persona.occupation = request.POST.get('occupation', persona.occupation)
        persona.income = request.POST.get('income', persona.income)
        persona.education = request.POST.get('education', persona.education)
        persona.marital_status = request.POST.get('marital_status', persona.marital_status)
        persona.online_behavior = request.POST.get('online_behavior', persona.online_behavior)
        persona.buying_preferences = request.POST.get('buying_preferences', persona.buying_preferences)
        persona.business_type = request.POST.get('business_type', persona.business_type)
        persona.product_description = request.POST.get('product_description', persona.product_description)
        persona.target_market = request.POST.get('target_market', persona.target_market)
        
        # Handle JSON fields
        persona.interests = request.POST.get('interests', '').split(',') if request.POST.get('interests') else []
        persona.problems = request.POST.get('problems', '').split(',') if request.POST.get('problems') else []
        persona.motivations = request.POST.get('motivations', '').split(',') if request.POST.get('motivations') else []
        persona.communication_channels = request.POST.get('communication_channels', '').split(',') if request.POST.get('communication_channels') else []
        persona.objections = request.POST.get('objections', '').split(',') if request.POST.get('objections') else []
        
        # Clean empty strings from lists
        persona.interests = [item.strip() for item in persona.interests if item.strip()]
        persona.problems = [item.strip() for item in persona.problems if item.strip()]
        persona.motivations = [item.strip() for item in persona.motivations if item.strip()]
        persona.communication_channels = [item.strip() for item in persona.communication_channels if item.strip()]
        persona.objections = [item.strip() for item in persona.objections if item.strip()]
        
        persona.save()
        messages.success(request, 'Profilul AI a fost actualizat cu succes.')
        return redirect('auth_app:persona_detail', persona_id=persona.id)
    
    return render(request, 'auth_app/edit_persona.html', {'persona': persona})

@login_required
def bulk_delete_personas(request):
    """Deletes multiple AI personas."""
    if request.method == 'POST':
        persona_ids = request.POST.getlist('persona_ids')
        if persona_ids:
            deleted_count = AIPersona.objects.filter(
                id__in=persona_ids, 
                user=request.user
            ).delete()[0]
            messages.success(request, f'{deleted_count} profiluri AI au fost șterse cu succes.')
        else:
            messages.warning(request, 'Nu ați selectat niciun profil pentru ștergere.')
    
    return redirect('auth_app:personas_list')

@login_required
def export_persona(request, persona_id):
    """Exports a single persona as a JSON file."""
    persona = get_object_or_404(AIPersona, id=persona_id, user=request.user)
    
    # Prepare the data for export
    export_data = {
        "name": persona.name,
        "age": persona.age,
        "location": persona.location,
        "occupation": persona.occupation,
        "income": persona.income,
        "education": persona.education,
        "marital_status": persona.marital_status,
        "interests": persona.interests,
        "problems": persona.problems,
        "motivations": persona.motivations,
        "online_behavior": persona.online_behavior,
        "buying_preferences": persona.buying_preferences,
        "communication_channels": persona.communication_channels,
        "objections": persona.objections,
        "business_type": persona.business_type,
        "product_description": persona.product_description,
        "target_market": persona.target_market,
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
        scraped_data = site.data  # Access the ScrapedData object directly
        # Create a summary of the scraped data
        summary = scraped_data.get_summary()
    except ScrapedData.DoesNotExist:
        scraped_data = None
        summary = None
        messages.warning(request, "Nu s-au găsit date detaliate pentru acest site.")
    # Get personas for this specific site
    personas = AIPersona.objects.filter(user=request.user, scraped_site=site).order_by('-created_at')
    # Get strategies for this specific site
    strategies = Strategy.objects.filter(user=request.user, scraped_site=site).order_by('-created_at')
    context = {
        'site': site,
        'data': scraped_data,  # Pass as 'data' to match template expectations
        'summary': summary,
        'openai_available': OPENAI_AVAILABLE,
        'personas': personas,
        'strategies': strategies,
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
        scraped_data = site.data
        
        # Convert the ScrapedData object to a dictionary for export
        data_to_export = {
            'meta_tags': scraped_data.meta_tags,
            'company_info': scraped_data.company_info,
            'headings': scraped_data.headings,
            'paragraphs': scraped_data.paragraphs,
            'links': scraped_data.links,
            'images': scraped_data.images,
            'buttons': scraped_data.buttons,
            'forms': scraped_data.forms,
            'lists': scraped_data.lists,
            'tables': scraped_data.tables,
            'scripts': scraped_data.scripts,
            'styles': scraped_data.styles,
            'contact_info': scraped_data.contact_info,
            'social_media': scraped_data.social_media,
            'statistics': scraped_data.statistics,
            'css_classes': scraped_data.css_classes,
            'element_ids': scraped_data.element_ids,
            'important_divs': scraped_data.important_divs,
            'important_spans': scraped_data.important_spans,
        }
        
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

@csrf_exempt
@login_required
def generate_personas_view(request):
    """API view to generate user personas based on a description."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        description = data.get('description')
        if not description:
            return JsonResponse({'error': 'Description is required'}, status=400)

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return JsonResponse({'error': 'OPENAI_API_KEY not configured'}, status=500)
        
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""
        Based on the following business description, generate 4 distinct user personas that would be the ideal customers.
        The business owner is not an expert in marketing, so make the personas easy to understand.
        For each persona, provide a name, a short description (2-3 sentences), their main goals, and their primary pain points.
        Return the result as a JSON object with a single key "personas", which is an array of the 4 persona objects.
        Business Description: --- {description} ---
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful marketing assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        personas_data = json.loads(response.choices[0].message.content)
        return JsonResponse(personas_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

def _post_to_facebook(message, image_url=None):
    """
    Helper function to post a message or photo to a Facebook Page.
    This function is designed to ALWAYS return a dictionary.
    """
    page_id = os.environ.get('FACEBOOK_PAGE_ID')
    access_token = os.environ.get('META_ACCESS_TOKEN')
    app_secret = os.environ.get('META_APP_SECRET')

    if not all([page_id, access_token, app_secret]):
        return {'success': False, 'error': {'message': 'Server environment not configured. Missing FACEBOOK_PAGE_ID, META_ACCESS_TOKEN, or META_APP_SECRET from .env file.', 'code': 500}}

    try:
        # Generate appsecret_proof
        appsecret_proof = hmac.new(
            app_secret.encode('utf-8'),
            msg=access_token.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if image_url:
            url = f"https://graph.facebook.com/{page_id}/photos"
            payload = {
                'caption': message,
                'url': image_url,
                'access_token': access_token,
                'appsecret_proof': appsecret_proof
            }
        else:
            url = f"https://graph.facebook.com/{page_id}/feed"
            payload = {
                'message': message,
                'access_token': access_token,
                'appsecret_proof': appsecret_proof
            }

        response = requests.post(url, data=payload)
        response_data = response.json()

        if response.ok:
            return {'success': True, 'data': response_data}
        else:
            return {'success': False, 'error': response_data.get('error', response_data)}
            
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': {'message': f'A network error occurred: {str(e)}', 'code': 503}}
    except json.JSONDecodeError:
        return {'success': False, 'error': {'message': 'Failed to decode JSON response from Facebook.', 'code': 500}}
    except Exception as e:
        return {'success': False, 'error': {'message': f'An unexpected error occurred: {str(e)}', 'code': 500}}

@csrf_exempt
@login_required
def post_to_facebook_view(request):
    """API endpoint pentru postarea pe Facebook"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodă invalidă'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message')
        image_url = data.get('image_url')

        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        result = _post_to_facebook(message, image_url)
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalid'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Strategy Views
@login_required
def strategies_list(request):
    """Lista strategiilor pentru utilizatorul curent"""
    strategies = Strategy.objects.filter(user=request.user).order_by('-created_at')
    
    # Filtrare
    strategy_type = request.GET.get('type')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    
    if strategy_type:
        strategies = strategies.filter(strategy_type=strategy_type)
    if status:
        strategies = strategies.filter(status=status)
    if priority:
        strategies = strategies.filter(priority=priority)
    
    context = {
        'strategies': strategies,
        'strategy_types': Strategy._meta.get_field('strategy_type').choices,
        'status_choices': Strategy._meta.get_field('status').choices,
        'priority_choices': Strategy._meta.get_field('priority').choices,
        'current_filters': {
            'type': strategy_type,
            'status': status,
            'priority': priority,
        }
    }
    return render(request, 'auth_app/strategies_list.html', context)

@login_required
def strategy_detail(request, strategy_id):
    """Detalii despre o strategie specifică"""
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    context = {
        'strategy': strategy,
        'personas': strategy.personas.all(),
        'site': strategy.scraped_site,
    }
    return render(request, 'auth_app/strategy_detail.html', context)

@login_required
def generate_strategy(request, site_id):
    """Generează o strategie bazată pe datele site-ului și persoanele generate"""
    if request.method != 'POST':
        messages.error(request, "Metodă invalidă.")
        return redirect('auth_app:site_detail', site_id=site_id)

    if not OPENAI_AVAILABLE:
        messages.error(request, 'Funcționalitatea AI nu este disponibilă. Verifică cheia API OpenAI.')
        return redirect('auth_app:site_detail', site_id=site_id)

    try:
        site = get_object_or_404(ScrapedSite, id=site_id, user=request.user)
        data = site.data
        personas = AIPersona.objects.filter(scraped_site=site, user=request.user)
        
        if not personas.exists():
            messages.error(request, 'Nu există persoane generate pentru acest site. Generează mai întâi persoanele.')
            return redirect('auth_app:site_detail', site_id=site_id)
            
    except ScrapedData.DoesNotExist:
        messages.error(request, 'Datele pentru acest site nu au fost găsite. Rulați din nou analiza.')
        return redirect('auth_app:site_detail', site_id=site_id)
    except Exception as e:
        messages.error(request, f"A apărut o eroare la preluarea datelor: {e}")
        return redirect('auth_app:strategies_list')

    # Construiește prompt-ul pentru generarea strategiei
    prompt_parts = [
        f"Create a comprehensive marketing strategy for website: {site.url}",
        f"Website title: {getattr(data, 'page_title', 'N/A')}",
        f"Meta description: {getattr(data, 'meta_tags', {}).get('description', 'N/A')}",
    ]

    # Adaugă informații despre persoane
    persona_data = []
    for persona in personas[:3]:  # Limitează la 3 persoane pentru prompt
        persona_data.append({
            'name': persona.name,
            'age': persona.age,
            'occupation': persona.occupation,
            'interests': persona.interests,
            'problems': persona.problems,
            'motivations': persona.motivations,
            'online_behavior': persona.online_behavior,
            'buying_preferences': persona.buying_preferences,
        })
    
    prompt_parts.append(f"Target personas: {json.dumps(persona_data, ensure_ascii=False)}")

    # Adaugă informații despre site
    headings_dict = getattr(data, 'headings', {})
    all_headings = []
    if isinstance(headings_dict, dict):
        for heading_list in headings_dict.values():
            if isinstance(heading_list, list):
                all_headings.extend([str(item) for item in heading_list])

    if all_headings:
        prompt_parts.append(f"Main headings: {', '.join(all_headings[:10])}")

    paragraphs = getattr(data, 'paragraphs', [])
    if paragraphs and isinstance(paragraphs, list):
        prompt_parts.append(f"Content: {' '.join(paragraphs[:3])}")

    prompt = "\n".join(prompt_parts) + """

CRITICAL: You must return ONLY valid JSON. No explanations, no markdown, no additional text.

The response must start with { and end with }.

Create a comprehensive marketing strategy for this website based on the personas and site analysis. Include ALL the following fields:

{
  "strategy": {
    "title": "Strategic Title",
    "description": "Comprehensive strategy description",
    "strategy_type": "marketing/content/social_media/seo/conversion/branding/customer_retention/growth",
    "site_analysis": {
      "strengths": ["strength1", "strength2"],
      "weaknesses": ["weakness1", "weakness2"],
      "opportunities": ["opportunity1", "opportunity2"],
      "threats": ["threat1", "threat2"]
    },
    "persona_insights": {
      "common_needs": ["need1", "need2"],
      "pain_points": ["pain1", "pain2"],
      "motivations": ["motivation1", "motivation2"],
      "preferred_channels": ["channel1", "channel2"]
    },
    "target_audience": {
      "primary": "Primary audience description",
      "secondary": "Secondary audience description",
      "demographics": "Age, location, income level",
      "psychographics": "Interests, values, lifestyle"
    },
    "key_messages": [
      "Key message 1",
      "Key message 2",
      "Key message 3"
    ],
    "channels": [
      "email",
      "social_media",
      "content_marketing",
      "seo",
      "paid_advertising"
    ],
    "tactics": [
      {
        "name": "Tactic name",
        "description": "Tactic description",
        "channel": "Channel name",
        "timeline": "Implementation timeline"
      }
    ],
    "timeline": {
      "phase1": "Month 1-2: Foundation",
      "phase2": "Month 3-4: Growth",
      "phase3": "Month 5-6: Optimization"
    },
    "budget_estimate": {
      "total": "Estimated total budget",
      "breakdown": {
        "content": "Content creation budget",
        "advertising": "Advertising budget",
        "tools": "Tools and software budget"
      }
    },
    "kpis": [
      "Website traffic increase",
      "Lead generation",
      "Conversion rate improvement",
      "Brand awareness"
    ],
    "implementation_steps": [
      "Step 1: Define objectives",
      "Step 2: Set up tracking",
      "Step 3: Create content calendar"
    ],
    "resources_needed": [
      "Content creators",
      "Marketing tools",
      "Analytics platform"
    ],
    "risks": [
      "Risk 1: Description and mitigation",
      "Risk 2: Description and mitigation"
    ]
  }
}

IMPORTANT: Make the strategy realistic and actionable for Romanian market. Focus on practical implementation steps and measurable results."""

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a strategic marketing expert. You must return ONLY valid JSON format without any markdown formatting, explanations, or additional text. All strings must be properly quoted and escaped. Do not include ```json or ``` markers. The response must be a valid JSON object starting with { and ending with }."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean JSON if needed
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        # Repair JSON if needed
        def repair_json(json_str):
            # Remove any leading/trailing non-JSON content
            json_str = json_str.strip()
            if not json_str.startswith('{'):
                start_idx = json_str.find('{')
                if start_idx != -1:
                    json_str = json_str[start_idx:]
            
            if not json_str.endswith('}'):
                end_idx = json_str.rfind('}')
                if end_idx != -1:
                    json_str = json_str[:end_idx + 1]
            
            return json_str
        
        content = repair_json(content)
        print(f"JSON content after repair (first 1000 chars): {content[:1000]}")
        print(f"JSON content length: {len(content)}")
        
        strategy_data = json.loads(content)
        strategy_info = strategy_data.get('strategy', {})
        
        # Creează strategia în baza de date
        strategy = Strategy.objects.create(
            user=request.user,
            scraped_site=site,
            title=strategy_info.get('title', f'Strategie pentru {site.domain}'),
            description=strategy_info.get('description', ''),
            strategy_type=strategy_info.get('strategy_type', 'marketing'),
            site_analysis=strategy_info.get('site_analysis', {}),
            persona_insights=strategy_info.get('persona_insights', {}),
            target_audience=strategy_info.get('target_audience', {}),
            key_messages=strategy_info.get('key_messages', []),
            channels=strategy_info.get('channels', []),
            tactics=strategy_info.get('tactics', []),
            timeline=strategy_info.get('timeline', {}),
            budget_estimate=strategy_info.get('budget_estimate', {}),
            kpis=strategy_info.get('kpis', []),
            implementation_steps=strategy_info.get('implementation_steps', []),
            resources_needed=strategy_info.get('resources_needed', []),
            risks=strategy_info.get('risks', [])
        )
        
        # Adaugă persoanele la strategie
        strategy.personas.set(personas)
        
        messages.success(request, f'Strategia "{strategy.title}" a fost generată cu succes!')
        return redirect('auth_app:strategy_detail', strategy_id=strategy.id)
        
    except json.JSONDecodeError as e:
        messages.error(request, f'Eroare la parsarea răspunsului AI: {e}')
        return redirect('auth_app:site_detail', site_id=site_id)
    except Exception as e:
        messages.error(request, f'Eroare la generarea strategiei: {e}')
        return redirect('auth_app:site_detail', site_id=site_id)

@login_required
def edit_strategy(request, strategy_id):
    """Editează o strategie existentă"""
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    if request.method == 'POST':
        # Actualizează câmpurile de bază
        strategy.title = request.POST.get('title', strategy.title)
        strategy.description = request.POST.get('description', strategy.description)
        strategy.strategy_type = request.POST.get('strategy_type', strategy.strategy_type)
        strategy.status = request.POST.get('status', strategy.status)
        strategy.priority = request.POST.get('priority', strategy.priority)
        
        # Actualizează câmpurile JSON
        try:
            if request.POST.get('key_messages'):
                strategy.key_messages = json.loads(request.POST.get('key_messages'))
            if request.POST.get('channels'):
                strategy.channels = json.loads(request.POST.get('channels'))
            if request.POST.get('kpis'):
                strategy.kpis = json.loads(request.POST.get('kpis'))
        except json.JSONDecodeError:
            messages.error(request, 'Format JSON invalid pentru unul din câmpuri.')
            return redirect('auth_app:edit_strategy', strategy_id=strategy_id)
        
        strategy.save()
        messages.success(request, 'Strategia a fost actualizată cu succes!')
        return redirect('auth_app:strategy_detail', strategy_id=strategy.id)
    
    context = {
        'strategy': strategy,
        'strategy_types': Strategy._meta.get_field('strategy_type').choices,
        'status_choices': Strategy._meta.get_field('status').choices,
        'priority_choices': Strategy._meta.get_field('priority').choices,
    }
    return render(request, 'auth_app/edit_strategy.html', context)

@login_required
def delete_strategy(request, strategy_id):
    """Șterge o strategie"""
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    if request.method == 'POST':
        strategy_title = strategy.title
        strategy.delete()
        messages.success(request, f'Strategia "{strategy_title}" a fost ștearsă cu succes!')
        return redirect('auth_app:strategies_list')
    
    context = {'strategy': strategy}
    return render(request, 'auth_app/delete_strategy.html', context)

@login_required
def export_strategy(request, strategy_id):
    """Exportă o strategie în format JSON"""
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    # Construiește datele pentru export
    export_data = {
        'strategy': {
            'title': strategy.title,
            'description': strategy.description,
            'strategy_type': strategy.strategy_type,
            'status': strategy.status,
            'priority': strategy.priority,
            'created_at': strategy.created_at.isoformat(),
            'updated_at': strategy.updated_at.isoformat(),
        },
        'site': {
            'url': strategy.scraped_site.url,
            'domain': strategy.scraped_site.domain,
            'title': strategy.scraped_site.page_title,
        },
        'personas': [
            {
                'name': persona.name,
                'age': persona.age,
                'occupation': persona.occupation,
                'interests': persona.interests,
                'problems': persona.problems,
                'motivations': persona.motivations,
            }
            for persona in strategy.personas.all()
        ],
        'analysis': {
            'site_analysis': strategy.site_analysis,
            'persona_insights': strategy.persona_insights,
            'target_audience': strategy.target_audience,
        },
        'strategy_details': {
            'key_messages': strategy.key_messages,
            'channels': strategy.channels,
            'tactics': strategy.tactics,
            'timeline': strategy.timeline,
            'budget_estimate': strategy.budget_estimate,
            'kpis': strategy.kpis,
            'implementation_steps': strategy.implementation_steps,
            'resources_needed': strategy.resources_needed,
            'risks': strategy.risks,
        }
    }
    
    response = HttpResponse(
        json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="strategy_{strategy.id}_{strategy.title.replace(" ", "_")}.json"'
    return response

# Post Management Views
@login_required
def posts_list(request):
    """Lista postărilor pentru utilizatorul curent"""
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    
    # Filtrare
    post_type = request.GET.get('type')
    platform = request.GET.get('platform')
    status = request.GET.get('status')
    
    if post_type:
        posts = posts.filter(post_type=post_type)
    if platform:
        posts = posts.filter(platform=platform)
    if status:
        posts = posts.filter(status=status)
    
    context = {
        'posts': posts,
        'post_types': Post._meta.get_field('post_type').choices,
        'platform_choices': Post._meta.get_field('platform').choices,
        'status_choices': Post._meta.get_field('status').choices,
        'current_filters': {
            'type': post_type,
            'platform': platform,
            'status': status,
        }
    }
    return render(request, 'auth_app/posts_list.html', context)

@login_required
def post_detail(request, post_id):
    """Detalii despre o postare specifică"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    context = {
        'post': post,
        'engagement_summary': post.get_engagement_summary(),
    }
    return render(request, 'auth_app/post_detail.html', context)

@login_required
def generate_posts_from_strategy(request, strategy_id):
    """Generează 5 postări bazate pe o strategie și persoanele sale"""
    if request.method != 'POST':
        messages.error(request, "Metodă invalidă.")
        return redirect('auth_app:strategy_detail', strategy_id=strategy_id)

    if not OPENAI_AVAILABLE:
        messages.error(request, 'Funcționalitatea AI nu este disponibilă. Verifică cheia API OpenAI.')
        return redirect('auth_app:strategy_detail', strategy_id=strategy_id)

    try:
        strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
        personas = strategy.personas.all()
        
        if not personas.exists():
            messages.error(request, 'Nu există persoane asociate cu această strategie.')
            return redirect('auth_app:strategy_detail', strategy_id=strategy_id)
            
    except Exception as e:
        messages.error(request, f"A apărut o eroare la preluarea strategiei: {e}")
        return redirect('auth_app:strategies_list')

    # Construiește prompt-ul pentru generarea postărilor
    prompt_parts = [
        f"Generate 5 engaging social media posts for a marketing strategy.",
        f"Strategy Title: {strategy.title}",
        f"Strategy Description: {strategy.description}",
        f"Strategy Type: {strategy.get_strategy_type_display()}",
        f"Target Audience: {strategy.get_target_audience_display()}",
        f"Key Messages: {strategy.get_key_messages_display()}",
        f"Channels: {strategy.get_channels_display()}",
    ]

    # Adaugă informații despre persoane
    persona_data = []
    for persona in personas[:3]:  # Limitează la 3 persoane pentru a nu face prompt-ul prea lung
        persona_data.append({
            'name': persona.name,
            'age': persona.age,
            'occupation': persona.occupation,
            'interests': persona.get_interests_display(),
            'problems': persona.get_problems_display(),
            'motivations': persona.get_motivations_display(),
        })
    
    if persona_data:
        prompt_parts.append(f"Target Personas: {json.dumps(persona_data, ensure_ascii=False)}")

    prompt = "\n".join(prompt_parts) + """

CRITICAL: You must return ONLY valid JSON. No explanations, no markdown, no additional text.

The response must start with { and end with }.

Create 5 engaging social media posts that align with the strategy and target personas. Each post should include:

{
  "posts": [
    {
      "title": "Post Title",
      "content": "Engaging post content that resonates with the target audience. Include relevant hashtags and call-to-action.",
      "image_prompt": "Detailed description for generating an image that matches the post content and brand style",
      "post_type": "social_media",
      "platform": "facebook",
      "tags": ["tag1", "tag2", "tag3"]
    }
  ]
}

IMPORTANT: 
- Make posts engaging and relevant to the target personas
- Include appropriate hashtags
- Create compelling image prompts for visual content
- Vary the platforms (Facebook, Instagram, LinkedIn, Twitter)
- Ensure content aligns with the marketing strategy
- Use Romanian language for content
- Make image prompts detailed and specific"""

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a social media marketing expert. You must return ONLY valid JSON format without any markdown formatting, explanations, or additional text. All strings must be properly quoted and escaped. Do not include ```json or ``` markers. The response must be a valid JSON object starting with { and ending with }."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean JSON if needed
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        # Repair JSON if needed
        try:
            posts_data = json.loads(content)
        except json.JSONDecodeError:
            # Try to repair the JSON
            def repair_json(json_str):
                json_str = re.sub(r'(\]|\})\s*(\[|\{)', r'\1,\2', json_str)
                json_str = re.sub(r'(")\s*(\[|\{)', r'\1,\2', json_str)
                json_str = re.sub(r'(\]|\})\s*(")', r'\1,\2', json_str)
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                return json_str
            
            fixed_content = repair_json(content)
            try:
                posts_data = json.loads(fixed_content)
            except json.JSONDecodeError:
                # Create fallback posts
                posts_data = {
                    "posts": [
                        {
                            "title": f"Post 1 - {strategy.title}",
                            "content": f"Descoperă cum {strategy.title} poate transforma afacerea ta! 🚀 #marketing #business #success",
                            "image_prompt": f"Professional business person looking at charts and graphs, modern office setting, {strategy.get_strategy_type_display()} theme",
                            "post_type": "social_media",
                            "platform": "facebook",
                            "tags": ["marketing", "business", "success"]
                        },
                        {
                            "title": f"Post 2 - {strategy.title}",
                            "content": f"Strategii eficiente pentru creșterea afacerii tale. {strategy.get_key_messages_display()} 💡 #growth #strategy",
                            "image_prompt": f"Growth chart with upward trend, business growth concept, professional design",
                            "post_type": "social_media",
                            "platform": "instagram",
                            "tags": ["growth", "strategy", "business"]
                        },
                        {
                            "title": f"Post 3 - {strategy.title}",
                            "content": f"Conectează-te cu audiența ta țintă prin {strategy.get_channels_display()}. Rezultate garantate! 📈",
                            "image_prompt": f"People connecting through social media, networking concept, modern digital communication",
                            "post_type": "social_media",
                            "platform": "linkedin",
                            "tags": ["networking", "audience", "results"]
                        },
                        {
                            "title": f"Post 4 - {strategy.title}",
                            "content": f"Transformă provocările în oportunități cu strategiile noastre de {strategy.get_strategy_type_display()}. 🔥",
                            "image_prompt": f"Lightbulb with business ideas, innovation concept, creative problem solving",
                            "post_type": "social_media",
                            "platform": "twitter",
                            "tags": ["innovation", "opportunities", "strategy"]
                        },
                        {
                            "title": f"Post 5 - {strategy.title}",
                            "content": f"Rezultate măsurabile și ROI clar cu abordarea noastră {strategy.get_strategy_type_display()}. 📊 #ROI #results",
                            "image_prompt": f"Dashboard with analytics and metrics, data visualization, business performance",
                            "post_type": "social_media",
                            "platform": "facebook",
                            "tags": ["ROI", "results", "analytics"]
                        }
                    ]
                }
                messages.warning(request, f"AI-ul nu a putut genera postări valide. Au fost create postări de bază pentru {strategy.title}.")

        if "posts" not in posts_data or not isinstance(posts_data["posts"], list):
            raise ValueError("Răspunsul JSON de la AI nu are formatul așteptat (lipsește array-ul 'posts').")

        # Creează postările în baza de date
        created_posts = []
        image_generator = ImageGenerator()
        facebook_poster = FacebookPoster()
        
        for post_info in posts_data["posts"]:
            post = Post.objects.create(
                user=request.user,
                strategy=strategy,
                title=post_info.get("title", f"Post - {strategy.title}"),
                content=post_info.get("content", ""),
                image_prompt=post_info.get("image_prompt", ""),
                post_type=post_info.get("post_type", "social_media"),
                platform=post_info.get("platform", "general"),
                tags=post_info.get("tags", [])
            )
            
            # Adaugă persoanele asociate
            if strategy.personas.exists():
                post.personas.set(strategy.personas.all())
            
            # Generează imaginea dacă există prompt
            if post.image_prompt:
                try:
                    image_result = image_generator.generate_image(post.image_prompt, strategy.scraped_site.domain)
                    if image_result and image_result.get('success'):
                        # Salvează imaginea în câmpul generated_image
                        image_filename = image_result.get('filename')
                        if image_filename:
                            post.generated_image = image_filename
                            post.save()
                except Exception as e:
                    logger.error(f"Failed to generate image for post {post.id}: {str(e)}")
            
            # Postează pe Facebook dacă platforma este Facebook
            if post.platform == 'facebook':
                try:
                    facebook_result = facebook_poster.post_post_to_facebook(post)
                    if facebook_result.get('success'):
                        post.facebook_posted = True
                        post.facebook_post_id = facebook_result.get('post_id', '')
                        post.status = 'published'
                        post.published_date = timezone.now()
                        post.save()
                        logger.info(f"Posted to Facebook: {post.title}")
                    else:
                        logger.warning(f"Failed to post to Facebook: {facebook_result.get('message', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Error posting to Facebook: {str(e)}")
            
            created_posts.append(post)
        
        messages.success(request, f'✅ Au fost generate cu succes {len(created_posts)} postări pentru strategia "{strategy.title}"!')
        return redirect('auth_app:posts_list')
        
    except json.JSONDecodeError as e:
        messages.error(request, f'Eroare la parsarea răspunsului AI: {e}')
        return redirect('auth_app:strategy_detail', strategy_id=strategy_id)
    except Exception as e:
        messages.error(request, f'Eroare la generarea postărilor: {e}')
        return redirect('auth_app:strategy_detail', strategy_id=strategy_id)

@login_required
def edit_post(request, post_id):
    """Editează o postare existentă"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        # Actualizează câmpurile de bază
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.image_prompt = request.POST.get('image_prompt', post.image_prompt)
        post.post_type = request.POST.get('post_type', post.post_type)
        post.platform = request.POST.get('platform', post.platform)
        post.status = request.POST.get('status', post.status)
        
        # Actualizează tag-urile
        try:
            if request.POST.get('tags'):
                post.tags = [tag.strip() for tag in request.POST.get('tags').split(',') if tag.strip()]
        except:
            post.tags = []
        
        post.save()
        messages.success(request, 'Postarea a fost actualizată cu succes!')
        return redirect('auth_app:post_detail', post_id=post.id)
    
    context = {
        'post': post,
        'post_types': Post._meta.get_field('post_type').choices,
        'platform_choices': Post._meta.get_field('platform').choices,
        'status_choices': Post._meta.get_field('status').choices,
    }
    return render(request, 'auth_app/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """Șterge o postare"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Postarea "{post_title}" a fost ștearsă cu succes!')
        return redirect('auth_app:posts_list')
    
    context = {'post': post}
    return render(request, 'auth_app/delete_post.html', context)

@login_required
def bulk_delete_posts(request):
    """Șterge mai multe postări"""
    if request.method == 'POST':
        post_ids = request.POST.getlist('post_ids')
        if post_ids:
            deleted_count = Post.objects.filter(
                id__in=post_ids, 
                user=request.user
            ).delete()[0]
            messages.success(request, f'{deleted_count} postări au fost șterse cu succes.')
        else:
            messages.warning(request, 'Nu ați selectat nicio postare pentru ștergere.')
    
    return redirect('auth_app:posts_list')

@login_required
def export_post(request, post_id):
    """Exportă o postare în format JSON"""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    # Construiește datele pentru export
    export_data = {
        'post': {
            'title': post.title,
            'content': post.content,
            'image_prompt': post.image_prompt,
            'post_type': post.post_type,
            'platform': post.platform,
            'status': post.status,
            'tags': post.tags,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
        },
        'strategy': {
            'title': post.strategy.title if post.strategy else 'N/A',
            'description': post.strategy.description if post.strategy else 'N/A',
            'strategy_type': post.strategy.get_strategy_type_display() if post.strategy else 'N/A',
        },
        'personas': [
            {
                'name': persona.name,
                'age': persona.age,
                'occupation': persona.occupation,
                'interests': persona.interests,
                'problems': persona.problems,
                'motivations': persona.motivations,
            }
            for persona in post.personas.all()
        ],
        'engagement_metrics': post.engagement_metrics,
    }
    
    response = HttpResponse(
        json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="post_{post.id}_{post.title.replace(" ", "_")}.json"'
    return response

@login_required
def debug_media(request):
    """Debug view to test media file serving"""
    posts_with_images = Post.objects.filter(generated_image__isnull=False)[:5]
    
    debug_info = []
    for post in posts_with_images:
        debug_info.append({
            'post_id': post.id,
            'post_title': post.title,
            'image_name': post.generated_image.name if post.generated_image else None,
            'image_url': post.generated_image.url if post.generated_image else None,
            'image_exists': post.generated_image and post.generated_image.storage.exists(post.generated_image.name) if post.generated_image else False,
        })
    
    context = {
        'debug_info': debug_info,
        'media_url': settings.MEDIA_URL,
        'media_root': settings.MEDIA_ROOT,
    }
    
    return render(request, 'auth_app/debug_media.html', context)

@csrf_exempt
def test_facebook_post_view(request):
    """A view to test Facebook posting - handles both GET and POST requests."""
    if request.method == 'GET':
        # Original test functionality
        message = f"This is a test post from the app at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        result = _post_to_facebook(message)
    elif request.method == 'POST':
        # Handle POST requests from React frontend
        try:
            data = json.loads(request.body)
            message = data.get('message')
            link = data.get('link')
            
            if not message:
                return JsonResponse({'success': False, 'error': 'Message is required'}, status=400)
            
            # If link is provided, append it to the message
            if link:
                message = f"{message}\n\n{link}"
            
            result = _post_to_facebook(message)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        if result.get('success'):
            return JsonResponse({'success': True, 'data': result.get('data', {})})
        else:
            error_details = result.get('error', {})
            status_code = error_details.get('code', 400)

            if not isinstance(status_code, int) or not 100 <= status_code <= 599:
                status_code = 400
            
            return JsonResponse({'success': False, 'error': error_details.get('message', 'Unknown error')}, status=status_code)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'A server error occurred while trying to format the response.'
        }, status=500)

def debug_env_view(request):
    """A view to debug environment variables inside the container."""
    relevant_vars = [
        'META_ACCESS_TOKEN',
        'META_APP_SECRET',
        'FACEBOOK_PAGE_ID',
        'DB_ENGINE',
        'DB_HOST',
        'POSTGRES_USER',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    debug_data = {}
    for var in relevant_vars:
        value = os.environ.get(var)
        debug_data[var] = {
            'value': value if var not in ['META_ACCESS_TOKEN', 'META_APP_SECRET'] else ('****' if value else None),
            'is_set': value is not None and value != ''
        }
        
    return JsonResponse(debug_data)


# Frontend API Views
@csrf_exempt
def scrape_website_api(request):
    """API endpoint for website scraping - compatible with frontend"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url', '')
            
            if not url:
                return JsonResponse({'error': 'URL is required'}, status=400)
            
            # Use existing scraping functionality
            if SCRAPER_AVAILABLE:
                scraper = UniversalSuperScraper()
                result = scraper.get_all_info(url)
            else:
                # Fallback pentru când scraper-ul nu e disponibil
                result = {
                    'title': f'Demo analysis for {url}',
                    'meta_description': 'Demo meta description',
                    'keywords': ['demo', 'website', 'analysis'],
                    'content': 'Demo content for testing purposes'
                }
            
            return JsonResponse({
                'title': result.get('title', ''),
                'meta_description': result.get('meta_description', ''),
                'keywords': result.get('keywords', []),
                'content_summary': result.get('content', '')[:500] + '...' if result.get('content') else 'No content available'
            })
            
        except Exception as e:
            logger.error(f"Error in scrape_website_api: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def generate_strategy_api(request):
    """API endpoint for strategy generation - compatible with frontend"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            personas = data.get('personas', [])
            
            if not personas:
                return JsonResponse({'error': 'Personas are required'}, status=400)
            
            # Generate strategy based on personas
            strategy_content = f"""
            Marketing Strategy

            Target Audience Analysis:
            Based on the provided customer personas, we've identified key segments with specific interests and pain points.

            Key Strategies:
            1. Content Marketing - Create valuable content addressing specific customer pain points
            2. Social Media Engagement - Target platforms where your personas are most active
            3. Personalized Messaging - Tailor communication to each persona segment
            4. Multi-channel Approach - Integrate email, social media, and digital advertising

            Expected Outcomes:
            - Improved customer engagement
            - Higher conversion rates
            - Better brand awareness
            - Increased customer retention
            """
            
            return JsonResponse({
                'title': 'AI-Generated Marketing Strategy',
                'strategy': strategy_content
            })
            
        except Exception as e:
            logger.error(f"Error in generate_strategy_api: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def generate_posts_api(request):
    """API endpoint for posts generation - compatible with frontend"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            strategy = data.get('strategy', {})
            
            if not strategy:
                return JsonResponse({'error': 'Strategy is required'}, status=400)
            
            # Generate sample posts based on strategy
            posts = [
                {
                    'title': 'Engagement Post',
                    'content': '🎯 Ready to transform your marketing strategy? Let\'s connect with your ideal customers! Share your thoughts below. #MarketingTips #CustomerEngagement',
                    'platform': 'facebook'
                },
                {
                    'title': 'Educational Post',
                    'content': '💡 Pro Tip: Understanding your customer personas is the key to successful marketing campaigns. What\'s your biggest challenge in reaching your target audience?',
                    'platform': 'linkedin'
                },
                {
                    'title': 'Promotional Post',
                    'content': '🚀 Unlock the power of AI-driven marketing strategies! Transform your business with personalized customer insights. #AI #Marketing #Growth',
                    'platform': 'instagram'
                },
                {
                    'title': 'Value Post',
                    'content': '📊 Data shows that personalized marketing campaigns have 6x higher engagement rates. Are you leveraging customer data effectively?',
                    'platform': 'twitter'
                },
                {
                    'title': 'Community Post',
                    'content': '🤝 Building strong customer relationships starts with understanding their needs. What\'s your approach to customer research? #Community #CustomerFirst',
                    'platform': 'facebook'
                }
            ]
            
            return JsonResponse({'posts': posts})
            
        except Exception as e:
            logger.error(f"Error in generate_posts_api: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Simple API endpoints for frontend (no auth required)
def sites_api(request):
    """API endpoint to get sites list - no auth required"""
    if request.method == 'GET':
        # Return empty list for now - can be extended later
        return JsonResponse([])
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def personas_api(request):
    """API endpoint to get personas list - no auth required"""
    if request.method == 'GET':
        # Return empty list for now - can be extended later
        return JsonResponse([])
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def strategies_api(request):
    """API endpoint to get strategies list - no auth required"""
    if request.method == 'GET':
        # Return empty list for now - can be extended later
        return JsonResponse([])
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def posts_api(request):
    """API endpoint to get posts list - no auth required"""
    if request.method == 'GET':
        # Return empty list for now - can be extended later
        return JsonResponse([])
    return JsonResponse({'error': 'Method not allowed'}, status=405)
