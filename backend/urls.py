from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importe a view de redirecionamento da raiz, se desejar que a raiz do site vá para /login/
# ou para a home do app core se o usuário estiver logado.
# from backend.core.views import index_redirect_view # Supondo que você tenha essa view
from backend.accounts.views import CustomLoginView, UserRegisterPageView, PasswordRecoveryView, UserProfileEditView, CustomLogoutView
from backend.core.views import HomePageView  # Adicione este import

urlpatterns = [
    path('admin/', admin.site.urls),
    # A raiz do site deve apontar para a view de login com nome 'login'
    path('', CustomLoginView.as_view(), name='login'),  # Corrigido para name='login'
    
    # Adiciona um alias global para a página de cadastro
    path('register/', UserRegisterPageView.as_view(), name='register_page'),

    # Adiciona um alias global para a página de recuperação de senha
    path('password-recovery/', PasswordRecoveryView.as_view(), name='password_recovery_page'),

    # Alias global para edição de perfil (corrige o erro do template)
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit_page'),

    # Alias global para home autenticada (resolve {% url 'core_home' %})
    path('home/', HomePageView.as_view(), name='core_home'),

    # Alias global para logout (resolve {% url 'logout' %})
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    # Inclui as URLs do app 'accounts'
    # Certifique-se de que 'backend.accounts.urls' existe e tem app_name = 'accounts'
    path('accounts/', include('backend.accounts.urls', namespace='accounts')),
    
    # Inclui as URLs do app 'core' com o namespace 'core'
    # Este é o ponto crucial para resolver o erro NoReverseMatch
    path('app/', include('backend.core.urls', namespace='core')), 
    
    # Inclui as URLs do app 'activities'
    # Certifique-se de que 'backend.activities.urls' existe e has app_name = 'activities'
    path('activities/', include('backend.activities.urls', namespace='activities')),
    # path('rifas/', include('backend.rifas.urls', namespace='rifas')),
    path('caronas/', include('backend.caronas.urls', namespace='caronas')),
    path('tasks/', include('backend.tasks.urls', namespace='tasks')),
    path('notifications_api/', include('backend.notifications.urls', namespace='notifications_api')), # Para APIs HTTP de notificações
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# É importante que o arquivo backend/core/urls.py tenha a linha:
# app_name = 'core'
# E o arquivo backend/accounts/urls.py tenha:
# app_name = 'accounts'
# E assim por diante para os outros apps.