# backend/urls.py ou djangoreactproject/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Importar views ou routers dos apps, se necessário incluí-los diretamente aqui
# (Mais comum incluir o urls.py do app)

urlpatterns = [
    # Rota para o painel administrativo do Django [2-4]
    path('admin/', admin.site.urls),

    # Rotas para obtenção e refresh de tokens JWT, essenciais para autenticação com o frontend React [2, 5-7]
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclui as URLs do aplicativo 'accounts' para gerenciamento de usuários, registro, login, logout e perfil [2, 5]
    # O accounts/urls.py conteria as rotas específicas como register/, login/, logout/, user/me/, users/<id>/ [2, 5, 7]
    path('api/auth/', include('accounts.urls')),

    # Inclui as URLs do aplicativo 'activities' para gerenciamento de eventos, escalas, equipes, etc. [2, 5]
    # O activities/urls.py conteria as rotas específicas para essas funcionalidades.
    path('api/activities/', include('activities.urls')),

    # Inclui as URLs do aplicativo 'rifas' para gerenciamento de rifas [2, 5]
    # O rifas/urls.py conteria as rotas específicas para rifas.
    path('api/rifas/', include('rifas.urls')), 

    # Inclui as URLs do aplicativo 'caronas' para gerenciamento de caronas [2, 5]
    # O caronas/urls.py conteria as rotas específicas para caronas.
    path('api/caronas/', include('caronas.urls')),

    # Exemplo de inclusão de URLs para um app 'customers' (visto em uma fonte) [3]
    # path('api/customers/', include('customers.urls')), [3]

    # Exemplo de inclusão de URLs para um app 'todo' (visto em outra fonte) [4]
    # path('api/todos/', include('todo.urls')), [4]

    # Rotas adicionais podem ser incluídas conforme a necessidade de outros apps [2, 5]
]

# Opcional: Incluir URLs do DRF para o browsable API login/logout, se você usar essa funcionalidade [8, 9]
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')), [8, 9]
# ]