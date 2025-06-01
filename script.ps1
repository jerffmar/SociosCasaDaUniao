# Script para criar/substituir arquivos do backend
# Execute este script a partir da pasta raiz do projeto.

$ErrorActionPreference = "Stop"

Function New-FileWithContent {
    param(
        [string]$RelativePath,
        [string]$Content
    )

    $FullPath = Join-Path -Path $PSScriptRoot -ChildPath $RelativePath
    $DirectoryPath = Split-Path -Path $FullPath

    if (-not (Test-Path -Path $DirectoryPath)) {
        New-Item -ItemType Directory -Path $DirectoryPath -Force | Out-Null
        Write-Host "Diretório criado: $DirectoryPath"
    }

    Set-Content -Path $FullPath -Value $Content -Force -Encoding UTF8
    Write-Host "Arquivo criado/substituído: $FullPath"
}

# --- backend/caronas/urls.py ---
$caronasUrlsContent = @'
# filepath: backend/caronas/urls.py
from django.urls import path
# from . import views # Descomente quando tiver views

urlpatterns = [
    # Adicione seus padrões de URL para caronas aqui
    # Exemplo: path('ofertas/', views.OfferListView.as_view(), name='offer-list'),
]
'@
New-FileWithContent -RelativePath "backend\caronas\urls.py" -Content $caronasUrlsContent

# --- backend/tasks/__init__.py ---
$tasksInitContent = @'
# filepath: backend/tasks/__init__.py
'@
New-FileWithContent -RelativePath "backend\tasks\__init__.py" -Content $tasksInitContent

# --- backend/tasks/apps.py ---
$tasksAppsContent = @'
# filepath: backend/tasks/apps.py
from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tasks'
'@
New-FileWithContent -RelativePath "backend\tasks\apps.py" -Content $tasksAppsContent

# --- backend/tasks/models.py ---
$tasksModelsContent = @'
# filepath: backend/tasks/models.py
from django.db import models

# Exemplo de modelo para tarefas, expanda conforme necessário
# class Task(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     due_date = models.DateTimeField(blank=True, null=True)
#     completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
'@
New-FileWithContent -RelativePath "backend\tasks\models.py" -Content $tasksModelsContent

# --- backend/tasks/views.py ---
$tasksViewsContent = @'
# filepath: backend/tasks/views.py
from django.shortcuts import render
# from rest_framework import generics
# from .models import Task # Descomente quando tiver modelos
# from .serializers import TaskSerializer # Descomente quando tiver serializers

# Exemplo de view, expanda conforme necessário
# class TaskListCreateView(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
'@
New-FileWithContent -RelativePath "backend\tasks\views.py" -Content $tasksViewsContent

# --- backend/tasks/serializers.py ---
$tasksSerializersContent = @'
# filepath: backend/tasks/serializers.py
# from rest_framework import serializers
# from .models import Task # Descomente quando tiver modelos

# Exemplo de serializer, expanda conforme necessário
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
'@
New-FileWithContent -RelativePath "backend\tasks\serializers.py" -Content $tasksSerializersContent

# --- backend/tasks/urls.py ---
$tasksUrlsContent = @'
# filepath: backend/tasks/urls.py
from django.urls import path
# from . import views # Descomente quando tiver views

urlpatterns = [
    # Adicione seus padrões de URL para tasks aqui
    # Exemplo: path('', views.TaskListCreateView.as_view(), name='task-list-create'),
]
'@
New-FileWithContent -RelativePath "backend\tasks\urls.py" -Content $tasksUrlsContent

# --- backend/tasks/admin.py ---
$tasksAdminContent = @'
# filepath: backend/tasks/admin.py
from django.contrib import admin
# from .models import Task # Descomente quando tiver modelos

# Exemplo de registro no admin, expanda conforme necessário
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('name', 'due_date', 'completed')
#     list_filter = ('completed', 'due_date')
#     search_fields = ('name', 'description')
'@
New-FileWithContent -RelativePath "backend\tasks\admin.py" -Content $tasksAdminContent

# --- backend/notifications/__init__.py ---
$notificationsInitContent = @'
# filepath: backend/notifications/__init__.py
'@
New-FileWithContent -RelativePath "backend\notifications\__init__.py" -Content $notificationsInitContent

# --- backend/notifications/apps.py ---
$notificationsAppsContent = @'
# filepath: backend/notifications/apps.py
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.notifications'
'@
New-FileWithContent -RelativePath "backend\notifications\apps.py" -Content $notificationsAppsContent

# --- backend/notifications/models.py ---
$notificationsModelsContent = @'
# filepath: backend/notifications/models.py
from django.db import models
# from django.conf import settings # Se for relacionar com User

# Exemplo de modelo para notificações, expanda conforme necessário
# class Notification(models.Model):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.username if hasattr(self, 'user') else 'Unknown User'}: {self.message[:20]}"
'@
New-FileWithContent -RelativePath "backend\notifications\models.py" -Content $notificationsModelsContent

# --- backend/notifications/views.py ---
$notificationsViewsContent = @'
# filepath: backend/notifications/views.py
from django.shortcuts import render
# from rest_framework import generics
# from .models import Notification # Descomente quando tiver modelos
# from .serializers import NotificationSerializer # Descomente quando tiver serializers

# Exemplo de view, expanda conforme necessário
# class NotificationListView(generics.ListAPIView):
#     serializer_class = NotificationSerializer
#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user).order_by('-created_at')
'@
New-FileWithContent -RelativePath "backend\notifications\views.py" -Content $notificationsViewsContent

# --- backend/notifications/serializers.py ---
$notificationsSerializersContent = @'
# filepath: backend/notifications/serializers.py
# from rest_framework import serializers
# from .models import Notification # Descomente quando tiver modelos

# Exemplo de serializer, expanda conforme necessário
# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ('id', 'message', 'is_read', 'created_at')
'@
New-FileWithContent -RelativePath "backend\notifications\serializers.py" -Content $notificationsSerializersContent

# --- backend/notifications/urls.py ---
$notificationsUrlsContent = @'
# filepath: backend/notifications/urls.py
from django.urls import path
# from . import views # Descomente quando tiver views

urlpatterns = [
    # Adicione seus padrões de URL para notifications aqui
    # Exemplo: path('', views.NotificationListView.as_view(), name='notification-list'),
]
'@
New-FileWithContent -RelativePath "backend\notifications\urls.py" -Content $notificationsUrlsContent

# --- backend/notifications/admin.py ---
$notificationsAdminContent = @'
# filepath: backend/notifications/admin.py
from django.contrib import admin
# from .models import Notification # Descomente quando tiver modelos

# Exemplo de registro no admin, expanda conforme necessário
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'message', 'is_read', 'created_at') # Remova 'user' se não estiver no modelo
#     list_filter = ('is_read', 'created_at')
#     search_fields = ('message',)
'@
New-FileWithContent -RelativePath "backend\notifications\admin.py" -Content $notificationsAdminContent

# --- backend/notifications/consumers.py ---
$notificationsConsumersContent = @'
# filepath: backend/notifications/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user = self.scope["user"] # Descomente se a autenticação estiver configurada
        # if not self.user.is_authenticated:
        #     await self.close()
        #     return

        # self.room_group_name = f'user_{self.user.id}_notifications'
        self.room_group_name = 'general_notifications' # Ou um grupo específico

        # Entrar no grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado ao servidor de notificações!'
        }))


    async def disconnect(self, close_code):
        # Sair do grupo da sala
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receber mensagem do WebSocket (do frontend) - opcional
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     # Lógica para lidar com mensagens recebidas do frontend, se necessário

    # Receber mensagem do grupo da sala (do backend)
    async def send_notification(self, event):
        message = event['message']
        # Enviar mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))
'@
New-FileWithContent -RelativePath "backend\notifications\consumers.py" -Content $notificationsConsumersContent

# --- backend/notifications/routing.py ---
$notificationsRoutingContent = @'
# filepath: backend/notifications/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
'@
New-FileWithContent -RelativePath "backend\notifications\routing.py" -Content $notificationsRoutingContent

# --- backend/asgi.py ---
$asgiContent = @'
# filepath: backend/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import backend.notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Obtenha a aplicação ASGI HTTP padrão primeiro.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            backend.notifications.routing.websocket_urlpatterns
        )
    ),
})
'@
New-FileWithContent -RelativePath "backend\asgi.py" -Content $asgiContent

Write-Host "Criação/substituição de arquivos concluída."