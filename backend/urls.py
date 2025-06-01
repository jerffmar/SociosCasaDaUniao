# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa settings para DEBUG
from django.conf.urls.static import static # Para servir static/media em dev
# Importa as views do simple_jwt diretamente no urls.py raiz,
# ou inclua-as a partir do urls.py do app accounts, como em algumas fontes.
# Vamos seguir a abordagem de incluir a partir do urls.py do app accounts,
# que é uma prática comum para manter a organização.
# Exemplo de como ficaria se fossem incluídas diretamente:
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
     TokenVerifyView,
     TokenBlacklistView,)

urlpatterns = [
    # URLs do site administrativo do Django [3, 4, 8, 12]
    path('admin/', admin.site.urls),

    # URLs de autenticação do DRF para a API navegável (opcional) [3, 13, 14]
    # Útil durante o desenvolvimento para testar a API diretamente no navegador.
    # path('api-auth/', include('rest_framework.urls')),

    # Prefixo para as URLs da API [9, 10, 12]
    path('api/', include([
        # Inclui as URLs do aplicativo accounts (autenticação, usuários) [3-5, 10]
        # O app accounts/urls.py conteria path('register/', ...), path('login/', ...), path('logout/', ...), path('users/me/', ...), etc.
        # E também poderia incluir os endpoints de token JWT, se não estiverem aqui.
        path('accounts/', include('accounts.urls')),

        # Inclui as URLs do aplicativo activities (eventos, escalas, equipes, relatórios) [3, 4]
        # activities/urls.py conteria path('events/', ...), path('scales/', ...), path('teams/', ...), path('reports/', ...), etc.
        path('activities/', include('activities.urls')),

        # Inclui as URLs do aplicativo rifas [3, 4]
        # rifas/urls.py conteria path('rifas/', ...), path('rifas/create/', ...), etc.
        path('rifas/', include('rifas.urls')),

        # Inclui as URLs do aplicativo caronas [3, 4]
        # caronas/urls.py conteria path('rides/offer/', ...), path('rides/find/', ...), etc.
        path('caronas/', include('caronas.urls')),

        # Opcional: Incluir URLs para tarefas assíncronas se houverem endpoints web para elas
         path('tasks/', include('tasks.urls')),

        # Inclui os endpoints de obtenção e refresh de token JWT [3, 9, 10]
        # Se estiverem definidos diretamente no urls.py do app accounts, remova daqui.
         path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
         path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        # Se estiver usando o blacklisting de tokens JWT (simple_jwt.token_blacklist),
        # as URLs de blacklisting podem ser incluídas aqui [3, 15].
        # path('token/blacklist/', include('token_blacklist.urls')),


    ])),

    # Configuração para servir arquivos estáticos e de mídia em ambiente de desenvolvimento [Não especificado nas fontes, mas prática comum]
    # Em produção, um servidor web (Nginx, Apache) ou um serviço de cloud (AWS S3, DigitalOcean Spaces) lidaria com isso.
    # As fontes mencionam servir estáticos do frontend via Django em produção [16, 17],
    # mas servir static/media do backend via Django em dev é padrão.
]

# Adicionar as URLs para arquivos de mídia apenas em DEBUG [Não especificado nas fontes, mas prática comum]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Nota: Para servir os arquivos estáticos do frontend React em produção,
# uma abordagem mencionada é ter uma view no Django que renderiza o index.html do build do React
# e configurar uma URL raiz (path('', views.index, name='index')) para essa view. [3, 16]
# Isso não é incluído acima pois a estrutura primária é a API.