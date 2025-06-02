from django.urls import path
from .views import (
    CustomLoginView, 
    UserRegisterView, 
    DirectPasswordResetAPIView, 
    UserProfileView,
    CustomTokenObtainPairView,
    CustomLogoutView
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'  # Adicione esta linha

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Adiciona a rota de login
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),  # Rota para login via API
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('password_reset/', DirectPasswordResetAPIView.as_view(), name='password_reset'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # URLs para JWT (se você estiver usando a API para login/token)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Adicione outras URLs específicas do app accounts aqui
    # Exemplo: path('password_reset_confirm/<uidb64>/<token>/', ..., name='password_reset_confirm'),
]
