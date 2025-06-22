#!/usr/bin/env python3
"""
Script pentru a posta postările pe Facebook cu imaginile lor sau doar text
"""

import os
import sys
import django
import requests
from pathlib import Path

# Load environment variables from .env file manually
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).resolve().parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment variables
load_env_file()

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

from auth_app.models import Post
from auth_app.facebook_poster import FacebookPoster

# Setează domeniul public pentru imagini (ngrok)
PUBLIC_DOMAIN = "https://4f1e-130-195-240-11.ngrok-free.app"

def post_posts_to_facebook():
    """Postează toate postările cu imagine pe Facebook"""
    
    # Verifică credențialele
    access_token = os.environ.get('META_ACCESS_TOKEN')
    page_id = os.environ.get('FACEBOOK_PAGE_ID')
    
    if not access_token or not page_id:
        print("❌ Credențialele Facebook nu sunt configurate!")
        print(f"Access Token: {'Setat' if access_token else 'Nu este setat'}")
        print(f"Page ID: {'Setat' if page_id else 'Nu este setat'}")
        return
    
    print("✅ Credențialele Facebook sunt configurate")
    print(f"Page ID: {page_id}")
    print(f"Access Token: {access_token[:20]}...")
    
    # Găsește toate postările cu imagine care nu sunt postate pe Facebook
    posts = Post.objects.filter(generated_image__isnull=False)
    
    print(f"\n📝 Găsite {posts.count()} postări cu imagine pentru a fi postate:\n")
    
    for post in posts:
        print(f"--- Postarea {post.id}: {post.title[:50]}... ---")
        
        if post.generated_image:
            # Construiește URL-ul public pentru imagine
            image_url = f"{PUBLIC_DOMAIN}{post.generated_image.url}"
            print(f"[INFO] Posting with image: {image_url}")
            photo_url = f"https://graph.facebook.com/{page_id}/photos"
            payload = {
                "caption": post.content or post.title,
                "url": image_url,
                "access_token": access_token
            }
            response = requests.post(photo_url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id')
                print(f"✅ Postat cu succes pe Facebook! ID: {post_id}")
                
                # Marchează postarea ca fiind postată pe Facebook
                post.facebook_posted = True
                post.facebook_post_id = post_id
                post.save()
            else:
                print(f"❌ Eroare la postare: {response.status_code}")
                print(f"Răspuns: {response.text}")
        else:
            # Postează doar textul
            print(f"[INFO] Posting text only: {post.content[:100]}...")
            feed_url = f"https://graph.facebook.com/{page_id}/feed"
            payload = {
                "message": post.content or post.title,
                "access_token": access_token
            }
            response = requests.post(feed_url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id')
                print(f"✅ Postat cu succes pe Facebook! ID: {post_id}")
                
                # Marchează postarea ca fiind postată pe Facebook
                post.facebook_posted = True
                post.facebook_post_id = post_id
                post.save()
            else:
                print(f"❌ Eroare la postare: {response.status_code}")
                print(f"Răspuns: {response.text}")
        
        print()
    
    print("🎉 Procesul de postare s-a terminat!")

if __name__ == "__main__":
    post_posts_to_facebook() 