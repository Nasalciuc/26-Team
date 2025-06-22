"""
Facebook Poster Module
Posts generated content to Facebook using Graph API
"""

import requests
import logging
from typing import Dict, Optional
from django.conf import settings

logger = logging.getLogger(__name__)

class FacebookPoster:
    def __init__(self, access_token: Optional[str] = None, page_id: Optional[str] = None):
        """
        Initialize Facebook Poster
        
        Args:
            access_token: Facebook access token (if None, tries to get from environment)
            page_id: Facebook page ID (if None, tries to get from environment)
        """
        self.access_token = access_token or getattr(settings, 'FACEBOOK_ACCESS_TOKEN', None)
        self.page_id = page_id or getattr(settings, 'FACEBOOK_PAGE_ID', '532394313287326')
        self.base_url = "https://graph.facebook.com"
        
        if not self.access_token:
            logger.warning("⚠️ No Facebook access token found. Will use mock responses.")
            self.mock_mode = True
        else:
            logger.info(f"✅ Facebook access token loaded: {self.access_token[:20]}...")
            self.mock_mode = False
    
    def post_to_facebook(self, message: str, link: str = None, image_url: str = None) -> Dict:
        """
        Post content to Facebook page
        
        Args:
            message: Text content to post
            link: Optional link to include
            image_url: Optional image URL to include
            
        Returns:
            Dictionary with posting results
        """
        logger.info(f"📘 Posting to Facebook: {message[:50]}...")
        
        if self.mock_mode:
            return self._get_mock_response(message)
        
        try:
            # Prepare the post data
            post_data = {
                'message': message,
                'access_token': self.access_token
            }
            
            # Add link if provided
            if link:
                post_data['link'] = link
            
            # Add image if provided
            if image_url:
                post_data['picture'] = image_url
            
            # Make request to Facebook Graph API
            url = f"{self.base_url}/{self.page_id}/feed"
            response = requests.post(url, data=post_data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"✅ Posted to Facebook successfully: {result.get('id', 'Unknown ID')}")
            
            return {
                'success': True,
                'post_id': result.get('id'),
                'message': 'Posted successfully to Facebook'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to post to Facebook: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to post to Facebook'
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error posting to Facebook: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error posting to Facebook'
            }
    
    def _get_mock_response(self, message: str) -> Dict:
        """
        Get mock response for testing without Facebook API
        """
        logger.info(f"🎭 Mock Facebook post: {message[:50]}...")
        return {
            'success': True,
            'post_id': 'mock_post_id_12345',
            'message': 'Mock post to Facebook (no API token)'
        }
    
    def post_post_to_facebook(self, post) -> Dict:
        """
        Post a Post object to Facebook
        
        Args:
            post: Post model instance
            
        Returns:
            Dictionary with posting results
        """
        # Create message from post content
        message = f"{post.title}\n\n{post.content}"
        
        # Add hashtags if available
        if post.tags:
            hashtags = ' '.join([f"#{tag.replace(' ', '')}" for tag in post.tags])
            message += f"\n\n{hashtags}"
        
        # Add link to the post detail page
        link = f"https://yourdomain.com/posts/{post.id}/"
        
        # Add image if available
        image_url = None
        if post.generated_image:
            image_url = f"https://yourdomain.com{post.generated_image.url}"
        
        return self.post_to_facebook(message, link, image_url) 