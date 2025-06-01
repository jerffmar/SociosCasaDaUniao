from django.urls import path
from .views import UserRegisterView
# Importe outras views de API de contas aqui, se necessário


urlpatterns = [
    path('cadastrar/', UserRegisterView.as_view(), name='api_cadastrar'),  # Alterado de 'register/' para 'cadastrar/'
    # Se você for usar JWT para este frontend também
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]