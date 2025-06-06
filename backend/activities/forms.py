from django import forms
from .models import Event, Escala
from backend.accounts.models import CustomUser
from django.core.exceptions import ValidationError

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
    leader = forms.ModelChoiceField(
        queryset=CustomUser.objects.all().order_by('first_name', 'last_name'),
        label='Dirigente',
        required=True,
        empty_label="Visitante",
    )
    assistant = forms.ModelChoiceField(
        queryset=CustomUser.objects.all().order_by('first_name', 'last_name'),
        label='Assistente',
        required=True,
        empty_label="Visitante",
        )
    details = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 500}), label='Detalhes', max_length=500, required=False)

    class Meta:
        model = Event
        fields = ['event_type', 'date', 'time', 'leader', 'assistant', 'details']

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get("leader")
        assistant = cleaned_data.get("assistant")

        if leader and assistant and leader == assistant:
            if leader.first_name != "Visitante":
                self.add_error('leader', "Dirigente e Assistente não podem ser a mesma pessoa.")
                self.add_error('assistant', "Dirigente e Assistente não podem ser a mesma pessoa.")
            

        return cleaned_data

class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala
        fields = [
            'titulo',
            'dificuldade',
            'risco',
            'previsao_duracao',
            'descricao_atividade',
        ]
        widgets = {
            'previsao_duracao': forms.TimeInput(attrs={'type': 'time'}),
            'descricao_atividade': forms.Textarea(attrs={'maxlength': 500}),
        }
