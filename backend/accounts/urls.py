from django.urls import path
from .views import (
    UserLoginView, 
    UserRegisterView, 
    UserProfileView, 
    DirectPasswordResetAPIView # Adicionar nova view
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password-reset/direct/', DirectPasswordResetAPIView.as_view(), name='direct-password-reset'),

    # Remova ou comente as URLs antigas de password reset:
    # path('password-reset/validate-user/', PasswordResetValidateUserView.as_view(), name='password-reset-validate-user'),
    # path('password-reset/set-new/', PasswordResetSetNewView.as_view(), name='password-reset-set-new'),
    # path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
