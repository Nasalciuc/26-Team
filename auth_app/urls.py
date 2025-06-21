from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scraping/', views.scraping_view, name='scraping'),
    path('sites/', views.site_list, name='site_list'),
    path('sites/<int:site_id>/', views.site_detail, name='site_detail'),
    path('sites/<int:site_id>/delete/', views.delete_site, name='delete_site'),
    path('sites/<int:site_id>/export/', views.export_site_data, name='export_site_data'),
] 