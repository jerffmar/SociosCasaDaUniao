from django import forms
from .models import Event
from backend.accounts.models import CustomUser

class EventForm(forms.ModelForm):
    EVENT_TYPES = [
        ('Sessão', 'Sessão'),
        ('Mutirão', 'Mutirão'),
        ('Preparo', 'Preparo'),
        ('Evento', 'Evento'),
    ]
    event_type = forms.ChoiceField(choices=EVENT_TYPES, label='Evento', widget=forms.HiddenInput)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    leader = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label='Dirigente', required=False, empty_label="Visitante")
    assistant = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label='Assistente', required=False, empty_label="Visitante")
    details = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 500}), label='Detalhes', max_length=500, required=False)

    class Meta:
        model = Event
        fields = ['event_type', 'date', 'time', 'leader', 'assistant', 'details']
