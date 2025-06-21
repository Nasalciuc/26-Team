from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class ScrapedSite(models.Model):
    """Model pentru a stoca informații despre site-urile scrapate"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scraped_sites')
    url = models.URLField(max_length=500)
    domain = models.CharField(max_length=255)
    page_title = models.CharField(max_length=500, blank=True, null=True)
    scraped_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'În așteptare'),
        ('processing', 'Se procesează'),
        ('completed', 'Completat'),
        ('failed', 'Eșuat')
    ], default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-scraped_at']
    
    def __str__(self):
        return f"{self.domain} - {self.scraped_at.strftime('%d.%m.%Y %H:%M')}"

class ScrapedData(models.Model):
    """Model pentru a stoca datele detaliate scrapate"""
    scraped_site = models.OneToOneField(ScrapedSite, on_delete=models.CASCADE, related_name='data')
    
    # Meta tags și informații de bază
    meta_tags = models.JSONField(default=dict, blank=True)
    company_info = models.JSONField(default=dict, blank=True)
    
    # Conținut text
    headings = models.JSONField(default=dict, blank=True)
    paragraphs = models.JSONField(default=list, blank=True)
    
    # Linkuri și resurse
    links = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True)
    
    # Elemente interactive
    buttons = models.JSONField(default=list, blank=True)
    forms = models.JSONField(default=list, blank=True)
    
    # Structuri de date
    lists = models.JSONField(default=list, blank=True)
    tables = models.JSONField(default=list, blank=True)
    
    # Resurse externe
    scripts = models.JSONField(default=list, blank=True)
    styles = models.JSONField(default=list, blank=True)
    
    # Informații de contact și social media
    contact_info = models.JSONField(default=dict, blank=True)
    social_media = models.JSONField(default=dict, blank=True)
    
    # Statistici și elemente speciale
    statistics = models.JSONField(default=list, blank=True)
    css_classes = models.JSONField(default=list, blank=True)
    element_ids = models.JSONField(default=list, blank=True)
    
    # Elemente importante
    important_divs = models.JSONField(default=list, blank=True)
    important_spans = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Date pentru {self.scraped_site.domain}"
    
    def get_summary(self):
        """Returnează un sumar al datelor scrapate"""
        return {
            'total_links': len(self.links),
            'total_images': len(self.images),
            'total_paragraphs': len(self.paragraphs),
            'total_headings': sum(len(headings) for headings in self.headings.values()),
            'has_contact_info': bool(self.contact_info),
            'has_social_media': bool(self.social_media),
            'total_tables': len(self.tables),
            'total_forms': len(self.forms)
        }

class AIPersona(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    location = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    income = models.CharField(max_length=100)
    education = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=100)
    interests = models.JSONField(default=list)
    problems = models.JSONField(default=list)
    motivations = models.JSONField(default=list)
    online_behavior = models.TextField()
    buying_preferences = models.TextField()
    communication_channels = models.JSONField(default=list)
    objections = models.JSONField(default=list)
    business_type = models.CharField(max_length=100)
    product_description = models.TextField()
    target_market = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def get_interests_display(self):
        """Returnează interesele ca string"""
        if isinstance(self.interests, list):
            return ', '.join(self.interests)
        return str(self.interests)

    def get_problems_display(self):
        """Returnează problemele ca string"""
        if isinstance(self.problems, list):
            return ', '.join(self.problems)
        return str(self.problems)

    def get_motivations_display(self):
        """Returnează motivațiile ca string"""
        if isinstance(self.motivations, list):
            return ', '.join(self.motivations)
        return str(self.motivations)

    def get_communication_channels_display(self):
        """Returnează canalele de comunicare ca string"""
        if isinstance(self.communication_channels, list):
            return ', '.join(self.communication_channels)
        return str(self.communication_channels)

    def get_objections_display(self):
        """Returnează obiecțiile ca string"""
        if isinstance(self.objections, list):
            return ', '.join(self.objections)
        return str(self.objections)
