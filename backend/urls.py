# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView # Adicione esta importação
from django.shortcuts import redirect # Adicionar para redirecionamento

from backend.accounts.views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Adicione esta linha para servir o index.html na raiz
    # path('', TemplateView.as_view(template_name='index.html'), name='spa_home'),
    # Modificado para redirecionar para /core/home/ se autenticado, senão para o SPA
    path('', lambda request: redirect('core:home') if request.user.is_authenticated else TemplateView.as_view(template_name='index.html')(request), name='root_dispatch'),

    path('admin/', admin.site.urls),

    # 1. Página de login padrão do Django em /login/ (para o admin e fallback)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Adicionado logout

    # 2. Outras URLs de autenticação do Django
    path('api/accounts/', include('backend.accounts.urls')), # Nova linha para alinhar com o SPA

    # URLs do app core (Página Home para usuários autenticados)
    path('core/', include('backend.core.urls')), # Nova linha

    # 3. API de Cadastro para o SPA em /cadastrar/
    path('cadastrar/', UserRegisterView.as_view(), name='api_cadastrar'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password_reset/success/', TemplateView.as_view(template_name='auth/password_reset_success.html'), name='password_reset_success'),
    # 4. APIs para o SPA
    path('api/', include([
        path('login/', TokenObtainPairView.as_view(), name='api_login_token_obtain_pair'), # Esta é /api/login/
        path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
        # Inclua outras URLs de API aqui
        # path('activities/', include('backend.activities.urls')),
        # path('rifas/', include('backend.rifas.urls')),
        # path('caronas/', include('backend.caronas.urls')),
        # path('tasks/', include('backend.tasks.urls')),
    # 5. Url para criação de nova senha após validação dos dados com sucesso
    ])),
    # A linha comentada abaixo não é mais necessária se você adicionou a de cima
    # path('', include('backend.core.urls')), # Exemplo, se 'core' app serve o index.html
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)