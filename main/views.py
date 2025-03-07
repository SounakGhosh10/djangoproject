from django.shortcuts import render
from django.http import JsonResponse

def index_view(request):
    return render(request, 'main/index.html')

# Health check endpoint for monitoring
def health_check(request):
    return JsonResponse({"status": "ok"})

# Admin views
def login_view(request):
    return render(request, 'main/login.html')

def dashboard_view(request):
    return render(request, 'main/dashboard.html')

def add_app_view(request):
    return render(request, 'main/add_app.html')

# User views
def user_login_view(request):
    return render(request, 'main/user_login.html')

def user_dashboard_view(request):
    return render(request, 'main/user_dashboard.html')

def user_tasks_view(request):
    return render(request, 'main/user_tasks.html')

def submit_task_view(request, app_id):
    return render(request, 'main/submit_task.html') 