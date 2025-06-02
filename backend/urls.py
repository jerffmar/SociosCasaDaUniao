from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # Inclui as URLs do app 'accounts'
    path('accounts/', include('backend.accounts.urls')),

    # Inclui as URLs do app 'core'
    path('core/', include('backend.core.urls')),

    # Configuração da URL raiz '/'
    # Exibe a página de login (index.html) para não autenticados e redireciona autenticados para 'core:home'
    path('', lambda request: redirect('core:home') if request.user.is_authenticated else TemplateView.as_view(template_name='index.html')(request), name='index'),
]

# Configuração para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)