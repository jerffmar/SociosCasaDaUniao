from django.urls import path
from .views import EventListAPIView, schedule_event, EscalaCreateView, EscalaUpdateView

app_name = 'activities'

urlpatterns = [
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('schedule_event/', schedule_event, name='schedule_event'),
    path('escala/', EscalaCreateView.as_view(), name='escala_list'),
    path('escala/edit/<int:pk>/', EscalaUpdateView.as_view(), name='escala_edit'),
]
