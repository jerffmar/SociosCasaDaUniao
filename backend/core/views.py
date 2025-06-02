from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

@login_required
def home_view(request):
    return render(request, 'core/home.html')

def index_redirect_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))  # 'home' é o name da sua URL para a página inicial
    else:
        # 'login' é o name da sua URL de login, conforme definido em accounts.urls
        # e referenciado em settings.LOGIN_URL
        return redirect(reverse('login'))

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Painel Principal'
        # Adicionar aqui lógica para buscar próximos eventos, dados do usuário, etc.
        # Exemplo:
        # context['proximos_eventos'] = Evento.objects.filter(data__gte=timezone.now()).order_by('data')[:5]
        return context

# Adicione outras views do app core aqui, se necessário
# Ex: def relatorio_eventos_view(request): ...