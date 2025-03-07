from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Extend the default Django user or create your own.
    # AbstractUser already has username, password, email, etc.
    is_admin = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

    # Avoid field name clashes with unique related_name values
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Add unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Add unique related_name
        blank=True
    )

    class Meta:
        db_table = 'users'

class App(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    package_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)

    class Meta:
        db_table = 'apps'

class Task(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
