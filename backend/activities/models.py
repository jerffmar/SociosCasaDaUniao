from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Escala(models.Model):
    titulo = models.CharField(max_length=200)
    dificuldade = models.CharField(
        max_length=10,
        choices=[
            ('Baixa', 'Baixa'),
            ('Media', 'Média'),
            ('Alta', 'Alta'),
        ]
    )
    risco = models.CharField(
        max_length=10,
        choices=[
            ('Baixo', 'Baixo'),
            ('Medio', 'Médio'),
            ('Alto', 'Alto'),
        ]
    )
    previsao_duracao = models.TimeField()
    descricao_atividade = models.TextField(max_length=500)

    def __str__(self):
        return self.titulo
