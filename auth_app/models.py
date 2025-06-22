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
    scraped_site = models.ForeignKey(ScrapedSite, on_delete=models.CASCADE, related_name='personas', null=True, blank=True)
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

class Strategy(models.Model):
    """Model pentru a stoca strategii de marketing bazate pe datele site-ului și persoanele generate"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strategies')
    scraped_site = models.ForeignKey(ScrapedSite, on_delete=models.CASCADE, related_name='strategies')
    personas = models.ManyToManyField(AIPersona, related_name='strategies', blank=True)
    
    # Informații de bază
    title = models.CharField(max_length=255)
    description = models.TextField()
    strategy_type = models.CharField(max_length=100, choices=[
        ('marketing', 'Strategie de Marketing'),
        ('content', 'Strategie de Conținut'),
        ('social_media', 'Strategie Social Media'),
        ('seo', 'Strategie SEO'),
        ('conversion', 'Strategie de Conversie'),
        ('branding', 'Strategie de Branding'),
        ('customer_retention', 'Strategie de Retenție Clienți'),
        ('growth', 'Strategie de Creștere'),
    ])
    
    # Analiza site-ului
    site_analysis = models.JSONField(default=dict, blank=True)
    
    # Analiza persoanelor
    persona_insights = models.JSONField(default=dict, blank=True)
    
    # Strategii detaliate
    target_audience = models.JSONField(default=dict, blank=True)
    key_messages = models.JSONField(default=list, blank=True)
    channels = models.JSONField(default=list, blank=True)
    tactics = models.JSONField(default=list, blank=True)
    timeline = models.JSONField(default=dict, blank=True)
    budget_estimate = models.JSONField(default=dict, blank=True)
    kpis = models.JSONField(default=list, blank=True)
    
    # Implementare
    implementation_steps = models.JSONField(default=list, blank=True)
    resources_needed = models.JSONField(default=list, blank=True)
    risks = models.JSONField(default=list, blank=True)
    
    # Status și prioritate
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Ciornă'),
        ('active', 'Activă'),
        ('implemented', 'Implementată'),
        ('paused', 'Pusă pe pauză'),
        ('completed', 'Finalizată'),
    ], default='draft')
    
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Scăzută'),
        ('medium', 'Medie'),
        ('high', 'Ridicată'),
        ('critical', 'Critică'),
    ], default='medium')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    implemented_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Strategies'
    
    def __str__(self):
        return f"{self.title} - {self.scraped_site.domain}"
    
    def get_strategy_summary(self):
        """Returnează un sumar al strategiei"""
        return {
            'total_personas': self.personas.count(),
            'strategy_type': self.get_strategy_type_display(),
            'status': self.get_status_display(),
            'priority': self.get_priority_display(),
            'days_since_creation': (timezone.now() - self.created_at).days,
        }
    
    def get_target_audience_display(self):
        """Returnează audiența țintă ca string"""
        if isinstance(self.target_audience, dict):
            return ', '.join([f"{k}: {v}" for k, v in self.target_audience.items()])
        return str(self.target_audience)
    
    def get_key_messages_display(self):
        """Returnează mesajele cheie ca string"""
        if isinstance(self.key_messages, list):
            return ', '.join(self.key_messages)
        return str(self.key_messages)
    
    def get_channels_display(self):
        """Returnează canalele ca string"""
        if isinstance(self.channels, list):
            return ', '.join(self.channels)
        return str(self.channels)

class Post(models.Model):
    """Model pentru a stoca postări generate bazate pe strategii și persoane"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    personas = models.ManyToManyField(AIPersona, related_name='posts', blank=True)
    
    # Informații de bază
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Conținutul postării")
    image_prompt = models.TextField(help_text="Prompt pentru generarea imaginii")
    
    # Tipul postării
    post_type = models.CharField(max_length=50, choices=[
        ('social_media', 'Social Media'),
        ('blog', 'Blog Post'),
        ('email', 'Email Marketing'),
        ('advertisement', 'Advertisement'),
        ('content_marketing', 'Content Marketing'),
    ], default='social_media')
    
    # Platforma țintă
    platform = models.CharField(max_length=50, choices=[
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('blog', 'Blog'),
        ('email', 'Email'),
        ('general', 'General'),
    ], default='general')
    
    # Status și programare
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Ciornă'),
        ('ready', 'Gata de publicare'),
        ('scheduled', 'Programată'),
        ('published', 'Publicată'),
        ('archived', 'Arhivată'),
    ], default='draft')
    
    # Programare
    scheduled_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Metadate
    tags = models.JSONField(default=list, blank=True)
    engagement_metrics = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.title} - {self.get_platform_display()}"
    
    def get_tags_display(self):
        """Returnează tag-urile ca string"""
        if isinstance(self.tags, list):
            return ', '.join(self.tags)
        return str(self.tags)
    
    def get_engagement_summary(self):
        """Returnează un sumar al metricilor de engagement"""
        if isinstance(self.engagement_metrics, dict):
            return {
                'likes': self.engagement_metrics.get('likes', 0),
                'shares': self.engagement_metrics.get('shares', 0),
                'comments': self.engagement_metrics.get('comments', 0),
                'views': self.engagement_metrics.get('views', 0),
            }
        return {'likes': 0, 'shares': 0, 'comments': 0, 'views': 0}
