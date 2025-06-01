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
