import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User

def create_superuser():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    if not password:
        print("Error: DJANGO_SUPERUSER_PASSWORD environment variable is not set.")
        return
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password, is_admin=True)
        print(f"Superuser '{username}' created successfully!")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == '__main__':
    create_superuser() 