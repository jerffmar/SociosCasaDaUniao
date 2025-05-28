from django.db import models

class Doador(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome

class Doacao(models.Model):
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_doacao = models.DateTimeField(auto_now_add=True)
    token_validacao = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'Doação de {self.valor} por {self.doador.nome}'