import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User

# Create admin user
admin_user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='adminpassword',
    is_staff=True,
    is_superuser=True,
    is_admin=True
)
admin_user.save()
print(f"Admin user created: {admin_user.username}")

# Create regular user
regular_user = User.objects.create_user(
    username='user',
    email='user@example.com',
    password='userpassword',
    is_staff=False,
    is_superuser=False,
    is_admin=False
)
regular_user.save()
print(f"Regular user created: {regular_user.username}")

print("Users created successfully!") 