#!/usr/bin/env python3
"""
Standalone Image Generator
A portable script that generates marketing images using OpenAI's DALL-E API
Can be used in any workspace or project
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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ImageGenerator:
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "generated_images"):
        """
        Initialize the Image Generator
        
        Args:
            api_key: OpenAI API key (if None, tries to get from environment)
            output_dir: Directory to save generated images
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.output_dir = Path(output_dir)
        self.base_url = "https://api.openai.com/v1"
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Check if API key is available
        if not self.api_key:
            print("⚠️ No OpenAI API key found. Will use mock responses.")
            self.mock_mode = True
        else:
            print(f"✅ OpenAI API key loaded: {self.api_key[:20]}...")
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
        print(f"🎨 Generating image: {description}")
        
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
            
            print("📤 Sending request to OpenAI DALL-E...")
            response = requests.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return self._get_mock_response(description)
            
            data = response.json()
            image_url = data['data'][0]['url']
            
            # Download and save the image
            saved_image = self._download_and_save_image(image_url, description)
            
            if saved_image:
                print(f"✅ Image generated successfully: {saved_image['filename']}")
                return {
                    'success': True,
                    'image_url': image_url,
                    'local_path': str(saved_image['path']),
                    'filename': saved_image['filename'],
                    'description': description,
                    'prompt': enhanced_prompt,
                    'business_name': business_name,
                    'generated_at': datetime.now().isoformat()
                }
            else:
                print("❌ Failed to download generated image")
                return self._get_mock_response(description)
                
        except Exception as e:
            print(f"❌ Image generation failed: {str(e)}")
            return self._get_mock_response(description)
    
    def _download_and_save_image(self, image_url: str, description: str) -> Optional[Dict]:
        """
        Download image from URL and save it locally
        
        Args:
            image_url: URL of the generated image
            description: Description for filename
            
        Returns:
            Dictionary with file info or None if failed
        """
        try:
            print("📥 Downloading generated image...")
            
            # Generate unique filename
            timestamp = int(time.time() * 1000)
            random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            filename = f"generated_{timestamp}_{random_id}.jpg"
            filepath = self.output_dir / filename
            
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Image saved: {filename}")
            return {
                'path': filepath,
                'filename': filename,
                'size': len(response.content)
            }
            
        except Exception as e:
            print(f"❌ Failed to download image: {str(e)}")
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
        filename = f"mock_generated_{timestamp}_{random_id}.jpg"
        
        print("🔄 Using mock response (no API key or API error)")
        
        return {
            'success': True,
            'image_url': f"https://picsum.photos/1024/1024?random={timestamp}",
            'local_path': str(self.output_dir / filename),
            'filename': filename,
            'description': description,
            'prompt': f"Mock generation for: {description}",
            'mock': True,
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_multiple_images(self, image_requests: list) -> list:
        """
        Generate multiple images from a list of requests
        
        Args:
            image_requests: List of dictionaries with 'description' and optional 'business_name'
            
        Returns:
            List of generation results
        """
        results = []
        
        print(f"🎨 Generating {len(image_requests)} images...")
        
        for i, request in enumerate(image_requests, 1):
            print(f"\n--- Image {i}/{len(image_requests)} ---")
            
            description = request.get('description', 'Professional business image')
            business_name = request.get('business_name', 'Business')
            
            result = self.generate_image(description, business_name)
            results.append(result)
            
            # Add delay between requests to avoid rate limiting
            if i < len(image_requests) and not self.mock_mode:
                print("⏱️ Waiting 2 seconds between requests...")
                time.sleep(2)
        
        successful = len([r for r in results if r.get('success')])
        print(f"\n✅ Completed: {successful}/{len(image_requests)} images generated successfully")
        
        return results
    
    def save_results_to_json(self, results: list, filename: str = "generation_results.json"):
        """
        Save generation results to a JSON file
        
        Args:
            results: List of generation results
            filename: Output filename
        """
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Results saved to: {filepath}")


def main():
    """
    Example usage and testing
    """
    print("🎯 Standalone Image Generator - Test Run")
    print("=" * 50)
    
    # Initialize generator
    generator = ImageGenerator()
    
    # Test single image generation
    print("\n🧪 Test 1: Single Image Generation")
    result = generator.generate_image(
        description="Elegant flower arrangement for a wedding, professional photography",
        business_name="Floral Dreams Studio"
    )
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test multiple image generation
    print("\n🧪 Test 2: Multiple Image Generation")
    image_requests = [
        {
            "description": "Modern coffee shop interior with customers enjoying coffee",
            "business_name": "Urban Coffee Co"
        },
        {
            "description": "Professional business team meeting in modern office",
            "business_name": "Tech Solutions Inc"
        },
        {
            "description": "Fresh ingredients for healthy cooking, vibrant colors",
            "business_name": "Healthy Eats Restaurant"
        }
    ]
    
    results = generator.generate_multiple_images(image_requests)
    
    # Save results
    generator.save_results_to_json(results)
    
    print("\n🎉 Test completed!")
    print(f"📁 Check the '{generator.output_dir}' folder for generated images")


if __name__ == "__main__":
    main()
