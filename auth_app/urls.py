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
    path('sites/<int:site_id>/generate-personas/', views.generate_personas_from_site, name='generate_personas_from_site'),
    path('sites/<int:site_id>/generate-strategy/', views.generate_strategy, name='generate_strategy'),
    
    # AI Personas
    path('ai-personas/', views.ai_personas_view, name='ai_personas'),
    path('personas/', views.personas_list, name='personas_list'),
    path('personas/<int:persona_id>/', views.persona_detail, name='persona_detail'),
    path('personas/<int:persona_id>/edit/', views.edit_persona, name='edit_persona'),
    path('personas/<int:persona_id>/delete/', views.delete_persona, name='delete_persona'),
    path('personas/<int:persona_id>/export/', views.export_persona, name='export_persona'),
    path('personas/bulk-delete/', views.bulk_delete_personas, name='bulk_delete_personas'),

    # Strategies
    path('strategies/', views.strategies_list, name='strategies_list'),
    path('strategies/<int:strategy_id>/', views.strategy_detail, name='strategy_detail'),
    path('strategies/<int:strategy_id>/edit/', views.edit_strategy, name='edit_strategy'),
    path('strategies/<int:strategy_id>/delete/', views.delete_strategy, name='delete_strategy'),
    path('strategies/<int:strategy_id>/export/', views.export_strategy, name='export_strategy'),

    # New AI and Social Media API Endpoints
    path('api/personas/generate/', views.generate_personas_view, name='generate_personas_api'),
    path('api/facebook/post/', views.post_to_facebook_view, name='post_to_facebook'),
    
    # Frontend API endpoints (no auth required)
    path('scrape-website/', views.scrape_website_api, name='scrape_website_api'),
    path('generate-personas-view/', views.generate_personas_view, name='generate_personas_view'),
    path('generate-strategy/', views.generate_strategy_api, name='generate_strategy_api'),
    path('generate-posts/', views.generate_posts_api, name='generate_posts_api'),
    path('facebook-post/', views.post_to_facebook_view, name='facebook_post_api'),
    
    # Frontend data endpoints (no auth required)
    path('api/sites/', views.sites_api, name='sites_api'),
    path('api/personas/', views.personas_api, name='personas_api'),
    path('api/strategies/', views.strategies_api, name='strategies_api'),
    path('api/posts/', views.posts_api, name='posts_api'),
    
    # Posts Management
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/export/', views.export_post, name='export_post'),
    path('posts/bulk-delete/', views.bulk_delete_posts, name='bulk_delete_posts'),
    path('strategies/<int:strategy_id>/generate-posts/', views.generate_posts_from_strategy, name='generate_posts_from_strategy'),
    
    # Debugging URLs
    path('test-facebook-post/', views.test_facebook_post_view, name='test_facebook_post'),
    path('debug-env/', views.debug_env_view, name='debug_env'),
] 