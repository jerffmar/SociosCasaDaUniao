from django.urls import path
from .views import HomePageView, home_view, index_redirect_view, events_api_view
from backend.accounts.views import UserProfileEditView  # Adicione este import

app_name = 'core'

urlpatterns = [
    path('', index_redirect_view, name='index_redirect'), # Redireciona da raiz do app
    path('home/', HomePageView.as_view(), name='home'), # Página principal autenticada
    # Alias global para home autenticada (resolve {% url 'core_home' %})
    path('home_global/', HomePageView.as_view(), name='core_home'),
    # Mantendo a view original home_view se ainda for usada em algum lugar ou para referência
    path('home_original/', home_view, name='core_home_original'),
    path('api/events/', events_api_view, name='api_events'), # API para buscar eventos (autenticado)
    # Alias global para edição de perfil (corrige o erro do template)
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit_page'),
]
