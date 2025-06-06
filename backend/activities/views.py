from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from .forms import EventForm
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

# Create your views here.
