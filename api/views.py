from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, App, Task
from .serializers import UserSerializer, AppSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import os
from django.conf import settings
from bson import ObjectId

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only admins to access certain endpoints.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """
        Override to handle ObjectId lookups
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        # Get the lookup value from the URL
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Try to convert the lookup value to an ObjectId
        try:
            object_id = ObjectId(lookup_value)
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, _id=object_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Exception as e:
            # If conversion fails, try the default behavior
            return super().get_object()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [permissions.AllowAny()]  # e.g., public can list or retrieve apps

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all tasks
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        # The user is the logged-in user
        user = request.user
        app_id = request.data.get('app_id')
        
        # Check if app exists
        try:
            app = get_object_or_404(App, _id=ObjectId(app_id))
        except Exception as e:
            return Response(
                {"detail": "Invalid app ID format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already has a pending or completed task for this app
        existing_task = Task.objects.filter(user=user, app=app).first()
        if existing_task:
            return Response(
                {"detail": f"You already have a {existing_task.status.lower()} task for this app."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle screenshot upload
        screenshot = request.FILES.get('screenshot')
        screenshot_path = ''
        
        if screenshot:
            # Create media directory if it doesn't exist
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Generate a unique filename
            filename = f"{user.username}_{app.name}_{screenshot.name}"
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            # Save the file
            with open(file_path, 'wb+') as destination:
                for chunk in screenshot.chunks():
                    destination.write(chunk)
            
            screenshot_path = filename
        
        # Create the task
        task = Task.objects.create(
            user=user,
            app=app,
            screenshot=screenshot_path,
            status='COMPLETED'  # Automatically mark as completed
        )
        
        # Add points to user
        user.points += app.points
        user.save()
        
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def upload_screenshot(self, request, pk=None):
        # For drag & drop file upload
        try:
            task = get_object_or_404(Task, _id=ObjectId(pk))
        except Exception as e:
            return Response(
                {"detail": "Invalid task ID format."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if task.user != request.user and not request.user.is_admin:
            return Response({"detail": "Not allowed."}, status=403)

        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "No file provided."}, status=400)
            
        # Create media directory if it doesn't exist
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Generate a unique filename
        filename = f"{task.user.username}_{task.app.name}_{file.name}"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Save the file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        task.screenshot = filename
        task.status = 'COMPLETED'  # Automatically mark as completed
        task.save()
        
        # Add points to user if not already added
        if task.status == 'PENDING':
            task.user.points += task.app.points
            task.user.save()
            
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Admin action to approve a task
        """
        if not request.user.is_admin:
            return Response({"detail": "Not allowed."}, status=403)
            
        try:
            task = get_object_or_404(Task, _id=ObjectId(pk))
        except Exception as e:
            return Response(
                {"detail": "Invalid task ID format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Only approve pending tasks
        if task.status != 'PENDING':
            return Response(
                {"detail": f"Task is already {task.status.lower()}."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        task.status = 'COMPLETED'
        task.save()
        
        # Add points to user
        task.user.points += task.app.points
        task.user.save()
        
        return Response(TaskSerializer(task).data)
