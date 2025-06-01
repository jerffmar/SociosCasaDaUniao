from django.urls import path
from .views import CustomLoginView, CustomLogoutView
# Se você tiver outras views de autenticação (ex: API com JWT), elas podem coexistir aqui.

urlpatterns = [
    # URLs para autenticação baseada em sessão/templates
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Mantenha suas URLs de API JWT aqui se elas já existirem e forem usadas por um frontend separado
    # Exemplo:
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
