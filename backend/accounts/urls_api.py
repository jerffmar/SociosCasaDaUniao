from django.urls import path
from .views import (
    UserLoginAPIView, UserRegisterAPIView, 
    PasswordResetRequestAPIView, PasswordResetConfirmAPIView # Adicionar PasswordResetConfirmAPIView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'), # NOVA ROTA
]