from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # Admin URLs
    path('custom-admin/login/', views.login_view, name='admin_login'),
    path('custom-admin/dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('custom-admin/add-app/', views.add_app_view, name='admin_add_app'),
    
    # User URLs
    path('user/login/', views.user_login_view, name='user_login'),
    path('user/dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('user/tasks/', views.user_tasks_view, name='user_tasks'),
    path('user/submit-task/<str:app_id>/', views.submit_task_view, name='submit_task'),
] 