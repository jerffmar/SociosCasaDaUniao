from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_redirect_view, name='index_redirect'), # Adicionado para a raiz
    path('home/', views.home_view, name='home'),
]