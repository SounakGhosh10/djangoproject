import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User, App

def seed_data():
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_admin=True
        )
        print("Admin user created successfully!")
    
    # Create regular user if it doesn't exist
    if not User.objects.filter(username='user').exists():
        User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword',
            is_admin=False
        )
        print("Regular user created successfully!")
    
    # Create sample apps if none exist
    if App.objects.count() == 0:
        sample_apps = [
            {
                'name': 'Facebook',
                'package_name': 'com.facebook.katana',
                'category': 'Social',
                'points': 10
            },
            {
                'name': 'Instagram',
                'package_name': 'com.instagram.android',
                'category': 'Social',
                'points': 15
            },
            {
                'name': 'Twitter',
                'package_name': 'com.twitter.android',
                'category': 'Social',
                'points': 12
            },
            {
                'name': 'LinkedIn',
                'package_name': 'com.linkedin.android',
                'category': 'Business',
                'points': 20
            },
            {
                'name': 'Uber',
                'package_name': 'com.ubercab',
                'category': 'Travel',
                'points': 25
            },
            {
                'name': 'Snapchat',
                'package_name': 'com.snapchat.android',
                'category': 'Social',
                'points': 15
            }
        ]
        
        for app_data in sample_apps:
            App.objects.create(**app_data)
        
        print(f"{len(sample_apps)} sample apps created successfully!")
    
    print("Data seeding completed!")

if __name__ == '__main__':
    seed_data() 