from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('debug-csrf/', views.debug_csrf, name='debug_csrf'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Site Info (simplified scraping)
    path('scraping/', views.scraping_view, name='scraping'),
    path('sites/', views.site_list, name='site_list'),
    path('sites/<int:site_id>/', views.site_detail, name='site_detail'),
    path('sites/<int:site_id>/delete/', views.delete_site, name='delete_site'),
    path('sites/<int:site_id>/export/', views.export_site_data, name='export_site_data'),
    path('sites/<int:site_id>/generate-personas/', views.generate_personas_from_site, name='generate_personas'),
    
    # AI Personas
    path('ai-personas/', views.ai_personas_view, name='ai_personas'),
    path('personas/', views.personas_list, name='personas_list'),
    path('personas/<int:persona_id>/', views.persona_detail, name='persona_detail'),
    path('personas/<int:persona_id>/delete/', views.delete_persona, name='delete_persona'),
    path('personas/<int:persona_id>/export/', views.export_persona, name='export_persona'),

    # New AI and Social Media Endpoints
    path('personas/generate/', views.generate_personas_view, name='generate_personas'),
    path('facebook/post/', views.post_to_facebook_view, name='post_to_facebook'),
] 