from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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