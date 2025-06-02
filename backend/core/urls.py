from django.urls import path
from .views import HomePageView

app_name = 'core'

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    # Adicione outras URLs do app core aqui
    # Ex: path('relatorios/eventos/', views.relatorio_eventos_view, name='relatorio_eventos'),
]