# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Importe as views da API diretamente aqui
# Certifique-se de que estas views existem em backend.accounts.views
from backend.accounts.views import (
    CustomTokenObtainPairView,  # Para /api/login/
    UserRegisterView,           # Para /api/register/
    UserProfileView,            # Para /api/accounts/profile/
    DirectPasswordResetAPIView  # Para /api/accounts/password-reset/direct/
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Redirecionamento da raiz: para /core/home/ se autenticado, senão serve o SPA (index.html)
    path('', lambda request: redirect('core:home') if request.user.is_authenticated else TemplateView.as_view(template_name='index.html')(request), name='root_dispatch'),

    # Admin do Django
    path('admin/', admin.site.urls),

    # URLs de autenticação padrão do Django (usadas principalmente pelo admin ou como fallback)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # URLs de redefinição de senha padrão do Django (para admin/fallback)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    # URLs da API
    path('api/', include([
        path('login/', CustomTokenObtainPairView.as_view(), name='api_login_token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
        path('register/', UserRegisterView.as_view(), name='api_register'), 
        path('accounts/profile/', UserProfileView.as_view(), name='api_user_profile'),
        path('accounts/password-reset/direct/', DirectPasswordResetAPIView.as_view(), name='api_direct_password_reset'),
        # Adicione outras URLs de API específicas de 'accounts' ou outros apps aqui
    ])),
    
    # URLs de apps Django (não API)
    path('core/', include('backend.core.urls')), # Assumindo que 'backend.core.urls' existe
    
    # Se você tiver URLs específicas do app 'accounts' que são para templates Django (não API)
    # e não estão cobertas acima, você pode incluí-las.
    # Exemplo: path('app-accounts/', include('backend.accounts.urls')),
    # Certifique-se que 'backend.accounts.urls' não defina rotas de API que já estão acima.
]

# Servir arquivos de mídia e estáticos durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # A linha abaixo para arquivos estáticos geralmente não é necessária se você tem
    # 'django.contrib.staticfiles' em INSTALLED_APPS e DEBUG=True,
    # pois o runserver lida com isso automaticamente.
    # No entanto, não prejudica tê-la.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)