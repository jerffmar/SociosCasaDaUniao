from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import calendar as py_calendar # Renomeado para evitar conflito com nome de variável
from backend.activities.models import Event

@login_required
def home_view(request):
    return render(request, 'core/home.html', {'user': request.user})  # Renderiza o template da página principal

def index_redirect_view(request):
    # Redireciona usuários autenticados para 'core:home' e não autenticados para 'accounts:login'
    if request.user.is_authenticated:
        return redirect(reverse('core:home'))
    else:
        return redirect(reverse('accounts:login'))

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Painel Principal'
        context['user'] = self.request.user
        # Adicionar aqui lógica para buscar próximos eventos, dados do usuário, etc.
        # Exemplo:
        # context['proximos_eventos'] = Evento.objects.filter(data__gte=timezone.now()).order_by('data')[:5]
        # Adicionando o nome do template da página de perfil para a sidebar
        context['profile_edit_page_name'] = 'profile_edit_page' # Substitua pelo nome real da sua URL de edição de perfil
        return context

# Nova view para fornecer dados de eventos para o calendário
@login_required
def events_api_view(request):
    """
    Fornece eventos para o calendário.
    Espera parâmetros 'month' e 'year' na query string.
    """
    try:
        month = int(request.GET.get('month')) # 1-12
        year = int(request.GET.get('year'))
    except (TypeError, ValueError):
        today = date.today()
        month = today.month
        year = today.year

    # Busca os eventos do models.Event
    events = Event.objects.filter(date__year=year, date__month=month)

    # Formata os eventos para o formato esperado pelo calendário
    formatted_events = {}
    for event in events:
        date_str = event.date.strftime("%Y-%m-%d")
        if date_str not in formatted_events:
            formatted_events[date_str] = []
        formatted_events[date_str].append({
            "id": event.id,
            "title": event.title,
            "time": event.time.strftime("%H:%M"),
            "type": "Sessão",  # Ajuste conforme necessário
            "team": "A Definir",  # Ajuste conforme necessário
            "description": event.description or "",
            "scale_items": [],  # Ajuste conforme necessário
            "snack_items": [],  # Ajuste conforme necessário
            "can_confirm_presence": event.date > date.today(),
            "user_team_matches": False  # Ajuste conforme necessário
        })

    return JsonResponse(formatted_events)

# Adicione outras views do app core aqui, se necessário
# Ex: def relatorio_eventos_view(request): ...