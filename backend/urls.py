# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
)

urlpatterns = [
    # URLs do site administrativo do Django [3, 4, 8, 12]
    path('admin/', admin.site.urls),

    # Inclui as URLs de autenticação baseadas em templates/sessão
    path('auth/', include('backend.accounts.urls')), # Movido para um prefixo 'auth/' para clareza

    # Inclui as URLs do app core (ex: página home)
    path('', include('backend.core.urls')), # Mapeia a raiz para as URLs do app 'core'

    # Inclui a URL de cadastro diretamente
    # Com esta inclusão, e o path 'cadastrar/' em accounts.urls_api, a URL final será /cadastrar/
    path('', include('backend.accounts.urls_api')), 

    # Prefixo para as OUTRAS URLs da API
    path('api/', include([
        # Suas URLs de API existentes, como activities, etc.
        # Removido: path('accounts/', include('backend.accounts.urls_api')),
        path('activities/', include('backend.activities.urls')),
        path('rifas/', include('backend.rifas.urls')),
        path('caronas/', include('backend.caronas.urls')),
        path('tasks/', include('backend.tasks.urls')),
        # ... seus outros includes de API ...
    ])),

    # Configuração para servir arquivos estáticos e de mídia em ambiente de desenvolvimento [Não especificado nas fontes, mas prática comum]
    # Em produção, um servidor web (Nginx, Apache) ou um serviço de cloud (AWS S3, DigitalOcean Spaces) lidaria com isso.
    # As fontes mencionam servir estáticos do frontend via Django em produção [16, 17],
    # mas servir static/media do backend via Django em dev é padrão.
]

# Adicionar as URLs para arquivos de mídia apenas em DEBUG [Não especificado nas fontes, mas prática comum]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Nota: Para servir os arquivos estáticos do frontend React em produção,
# uma abordagem mencionada é ter uma view no Django que renderiza o index.html do build do React
# e configurar uma URL raiz (path('', views.index, name='index')) para essa view. [3, 16]
# Isso não é incluído acima pois a estrutura primária é a API.