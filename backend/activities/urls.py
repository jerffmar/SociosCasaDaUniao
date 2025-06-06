from django.urls import path
from .views import EventListAPIView, schedule_event

app_name = 'activities'

urlpatterns = [
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('schedule_event/', schedule_event, name='schedule_event'),
]
