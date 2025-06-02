from django.urls import path
from .views import (
    UserLoginView,  # View para login via API
    UserRegisterView, 
    DirectPasswordResetAPIView,
    UserProfileView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # Rota para login via API
    path('register/', UserRegisterView.as_view(), name='register'),
    path('password-reset/', DirectPasswordResetAPIView.as_view(), name='password_reset'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]