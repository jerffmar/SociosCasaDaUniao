from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Importe as views da API que serão usadas diretamente aqui
from backend.accounts.views import (
    UserRegisterView, 
    UserProfileView, 
    DirectPasswordResetAPIView,
    CustomTokenObtainPairView # Assumindo que está em accounts.views
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', lambda request: redirect('core:home') if request.user.is_authenticated else TemplateView.as_view(template_name='index.html')(request), name='root_dispatch'),
    path('admin/', admin.site.urls),

    # URLs de autenticação Django padrão (para admin e fallback)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # URLs de redefinição de senha Django padrão (se ainda as usar para o admin, por exemplo)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password_reset/success/', TemplateView.as_view(template_name='auth/password_reset_success.html'), name='password_reset_success'),
    # Adicione outras URLs de password reset do Django se necessário (confirm, done, etc.)

    # URLs da API
    path('api/', include([
        path('login/', CustomTokenObtainPairView.as_view(), name='api_login_token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
        path('register/', UserRegisterView.as_view(), name='api_register'), 
        path('accounts/profile/', UserProfileView.as_view(), name='api_user_profile'), # <<< ADICIONADO AQUI
        path('accounts/password-reset/direct/', DirectPasswordResetAPIView.as_view(), name='api_direct_password_reset'),
    ])),
    
    # URLs de apps Django (não API)
    path('core/', include('backend.core.urls')),
    # Se você tiver URLs específicas do app 'accounts' que não são API e não estão cobertas acima:
    # path('accounts/', include('backend.accounts.urls')), # Cuidado com sobreposições
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
