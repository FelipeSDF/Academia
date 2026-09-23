from django.db import models

class Peso(models.Model):
    class Tipo(models.TextChoices):
        HALTER = 'HAL', 'Halter'
        ANILHA = 'ANI', 'Anilha'
        BARRA = 'BAR', 'Barra'
        KETTLEBELL = 'KET', 'Kettlebell'
        CANELEIRA = 'CAN', 'Caneleira'

    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    valor = models.FloatField()
    date = models.DateField()
    tipo = models.CharField(
        max_length=3,
        choices=Tipo.choices,
        default=Tipo.HALTER,
    )

    def __str__(self):
        return self.nome
