from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # Inclui as URLs do app 'accounts'
    path('accounts/', include('backend.accounts.urls')),

    # Inclui as URLs do app 'core'
    path('core/', include('backend.core.urls')),

    # Inclui as rotas da API
    path('api/', include('backend.accounts.urls_api')),  # Certifique-se de que urls_api.py está configurado

    # Configuração da URL raiz '/'
    path('', lambda request: redirect('core:home') if request.user.is_authenticated else redirect('accounts:login'), name='index'),
]

# Configuração para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)