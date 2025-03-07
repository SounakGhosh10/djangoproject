from rest_framework import serializers
from .models import User, App, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'points', 'is_admin']

class AppSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        return str(obj._id) if obj._id else None
    
    class Meta:
        model = App
        fields = ['id', 'name', 'package_name', 'category', 'points']

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    app = AppSerializer(read_only=True)
    
    def get_id(self, obj):
        return str(obj._id) if obj._id else None
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'app', 'screenshot', 'status', 'created_at', 'updated_at']
