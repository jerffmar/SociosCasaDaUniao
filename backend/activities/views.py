from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView  # Import UpdateView
from django.views.generic.list import ListView  # Import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Event, Escala
from .serializers import EventSerializer
from .forms import EventForm, EscalaForm
from rest_framework.permissions import IsAuthenticated

class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if month and year:
            return Event.objects.filter(date__month=month, date__year=year)
        else:
            return Event.objects.all()

@login_required
def schedule_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('core_home')  # Redireciona para a página do calendário
    else:
        form = EventForm()
    return render(request, 'schedule_event.html', {'form': form})

class EventCreateView(PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'activities/event_create.html'
    success_url = reverse_lazy('core:home')  # Redireciona para a home após a criação
    permission_required = 'activities.add_event'  # Permissão necessária

    def handle_no_permission(self):
        return redirect('core:home')  # Redireciona para a home se não tiver permissão

class EscalaListView(PermissionRequiredMixin, ListView):
    model = Escala
    template_name = 'activities/escala_list.html'
    context_object_name = 'escalas'
    permission_required = 'activities.add_escala'

class EscalaCreateView(PermissionRequiredMixin, CreateView):
    model = Escala
    form_class = EscalaForm
    template_name = 'activities/escala_list.html'  # Use o mesmo template para listar e criar
    success_url = reverse_lazy('activities:escala_list')  # Redireciona para a listagem após a criação
    permission_required = 'activities.add_escala'  # Permissão necessária

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['escalas'] = Escala.objects.all()  # Adiciona a lista de escalas ao contexto
        context['form'] = EscalaForm() # Garante que o formulário esteja no contexto
        return context

    def handle_no_permission(self):
        return redirect('core:home')  # Redireciona para a home se não tiver permissão

class EscalaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Escala
    form_class = EscalaForm
    template_name = 'activities/escala_edit.html'
    success_url = reverse_lazy('activities:escala_list')
    permission_required = 'activities.change_escala'

    def handle_no_permission(self):
        return redirect('core:home')
