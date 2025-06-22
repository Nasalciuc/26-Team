"""
Image Generator Module for Django App
Generates marketing images using OpenAI's DALL-E API for social media posts
"""

import os
import requests
import json
import time
import random
import string
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Image Generator
        
        Args:
            api_key: OpenAI API key (if None, tries to get from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"
        
        # Check if API key is available
        if not self.api_key:
            logger.warning("No OpenAI API key found. Will use mock responses.")
            self.mock_mode = True
        else:
            logger.info(f"OpenAI API key loaded: {self.api_key[:20]}...")
            self.mock_mode = False
    
    def enhance_prompt(self, description: str, business_name: str = "Business") -> str:
        """
        Enhance the image generation prompt for better marketing results
        
        Args:
            description: Basic image description
            business_name: Name of the business (for context)
            
        Returns:
            Enhanced prompt for better image generation
        """
        enhanced = f"""Create a professional, high-quality marketing image for "{business_name}". {description}. 
        Style: Modern, clean, commercial photography style. High resolution, good lighting, appealing composition. 
        Suitable for social media marketing. No text or logos in the image."""
        
        return enhanced.strip()
    
    def generate_image(self, description: str, business_name: str = "Business") -> Dict:
        """
        Generate an image using DALL-E 3
        
        Args:
            description: Description of the image to generate
            business_name: Business name for context
            
        Returns:
            Dictionary with generation results
        """
        logger.info(f"Generating image: {description}")
        
        if self.mock_mode:
            return self._get_mock_response(description)
        
        try:
            enhanced_prompt = self.enhance_prompt(description, business_name)
            
            # Make request to OpenAI DALL-E API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "dall-e-3",
                "prompt": enhanced_prompt,
                "size": "1024x1024",
                "quality": "standard",
                "n": 1
            }
            
            logger.info("Sending request to OpenAI DALL-E...")
            response = requests.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"API Error {response.status_code}: {response.text}")
                return self._get_mock_response(description)
            
            data = response.json()
            image_url = data['data'][0]['url']
            
            # Download and save the image
            saved_image = self._download_and_save_image(image_url, description)
            
            if saved_image:
                logger.info(f"Image generated successfully: {saved_image['filename']}")
                return {
                    'success': True,
                    'image_url': image_url,
                    'local_path': saved_image['path'],
                    'filename': saved_image['filename'],
                    'description': description,
                    'prompt': enhanced_prompt,
                    'business_name': business_name,
                    'generated_at': datetime.now().isoformat()
                }
            else:
                logger.error("Failed to download generated image")
                return self._get_mock_response(description)
                
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return self._get_mock_response(description)
    
    def _download_and_save_image(self, image_url: str, description: str) -> Optional[Dict]:
        """
        Download image from URL and save it to Django media storage
        
        Args:
            image_url: URL of the generated image
            description: Description for filename
            
        Returns:
            Dictionary with file info or None if failed
        """
        try:
            logger.info("Downloading generated image...")
            
            # Generate unique filename
            timestamp = int(time.time() * 1000)
            random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            filename = f"generated_images/generated_{timestamp}_{random_id}.jpg"
            
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Save to Django media storage
            file_content = ContentFile(response.content)
            saved_path = default_storage.save(filename, file_content)
            
            logger.info(f"Image saved: {saved_path}")
            return {
                'path': saved_path,
                'filename': filename,
                'size': len(response.content)
            }
            
        except Exception as e:
            logger.error(f"Failed to download image: {str(e)}")
            return None
    
    def _get_mock_response(self, description: str) -> Dict:
        """
        Generate a mock response when API is not available
        
        Args:
            description: Image description
            
        Returns:
            Mock response dictionary
        """
        timestamp = int(time.time() * 1000)
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        filename = f"generated_images/mock_generated_{timestamp}_{random_id}.jpg"
        
        logger.info("Using mock response (no API key or API error)")
        
        return {
            'success': True,
            'image_url': f"https://picsum.photos/1024/1024?random={timestamp}",
            'local_path': filename,
            'filename': filename,
            'description': description,
            'prompt': f"Mock generation for: {description}",
            'mock': True,
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_images_for_posts(self, posts: list) -> list:
        """
        Generate images for a list of posts
        
        Args:
            posts: List of Post objects with image_prompt field
            
        Returns:
            List of generation results
        """
        results = []
        
        logger.info(f"Generating images for {len(posts)} posts...")
        
        for i, post in enumerate(posts, 1):
            logger.info(f"--- Image {i}/{len(posts)} ---")
            
            if not post.image_prompt:
                logger.warning(f"Post {post.id} has no image prompt, skipping...")
                continue
            
            # Use strategy title as business name if available
            business_name = post.strategy.title if post.strategy else "Business"
            
            result = self.generate_image(post.image_prompt, business_name)
            result['post_id'] = post.id
            results.append(result)
            
            # Add delay between requests to avoid rate limiting
            if i < len(posts) and not self.mock_mode:
                logger.info("Waiting 2 seconds between requests...")
                time.sleep(2)
        
        successful = len([r for r in results if r.get('success')])
        logger.info(f"Completed: {successful}/{len(results)} images generated successfully")
        
        return results 