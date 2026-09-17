from django.db import models

# Create your models here.
class Livro(models.Model):
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    date = models.DateField(max_length=100)
    valor = models.FloatField()

    def __str__(self):
        return self.nome

