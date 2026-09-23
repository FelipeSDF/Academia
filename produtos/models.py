from django.db import models

class Produto(models.Model):
    class Tipo(models.TextChoices):
        ALIMENTO = 'ALI', 'Alimento'
        BEBIDA = 'BEB', 'Bebida'
        LIMPEZA = 'LIM', 'Limpeza'
        HIGIENE = 'HIG', 'Higiene'
        PAPELARIA = 'PAP', 'Papelaria'

    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    valor = models.FloatField()
    date = models.DateField()
    tipo = models.CharField(
        max_length=3,
        choices=Tipo.choices,
        default=Tipo.ALIMENTO,
    )

    def __str__(self):
        return self.nome
