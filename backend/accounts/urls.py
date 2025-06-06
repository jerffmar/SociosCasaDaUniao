from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,  # Certifique-se de importar
    UserRegisterPageView,
    PasswordRecoveryView,
    UserProfileEditView,
    # API Views - podem ser agrupadas sob um prefixo /api/ se desejado
    UserRegisterAPIView,
    UserLoginView as UserLoginAPIView, # Renomear para evitar conflito se CustomLoginView for usada aqui
    CustomTokenObtainPairView,
    UserProfileView as UserProfileAPIView,
    DirectPasswordResetAPIView,
    LogoutAPIView,  # Importando a nova view para logout da API
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # URLs para páginas renderizadas por template
    path('login/', CustomLoginView.as_view(), name='login'), # Rota específica para login dentro de /accounts/
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Garante que o método seja GET e POST
    path('register/', UserRegisterPageView.as_view(), name='register_page'),
    path('password-recovery/', PasswordRecoveryView.as_view(), name='password_recovery_page'),
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit_page'),

    # URLs para API (geralmente prefixadas com /api/ no urls.py principal ou aqui)
    # Exemplo de como poderiam ser organizadas aqui:
    path('api/register/', UserRegisterAPIView.as_view(), name='api_user_register'),
    path('api/login/', UserLoginAPIView.as_view(), name='api_user_login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', UserProfileAPIView.as_view(), name='api_user_profile'),
    path('api/password-reset/', DirectPasswordResetAPIView.as_view(), name='api_direct_password_reset'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),  # Adicionando a URL para logout da API
]
