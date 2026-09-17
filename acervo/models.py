from django.db import models

class Livro(models.Model):
    class Classificacao(models.TextChoices):
        GENERALIDADES = '000', '000 – Generalidades e Informação'
        FILOSOFIA = '100', '100 – Filosofia e Psicologia'
        RELIGIAO = '200', '200 – Religião e Teologia'
        CIENCIAS_SOCIAIS = '300', '300 – Ciências Sociais e Direito'
        LINGUISTICA = '400', '400 – Linguística e Idiomas'
        CIENCIAS_PURAS = '500', '500 – Ciências Puras'
        CIENCIAS_APLICADAS = '600', '600 – Ciências Aplicadas'
        ARTES = '700', '700 – Artes e Recreação'
        LITERATURA = '800', '800 – Literatura'
        HISTORIA = '900', '900 – História e Geografia'

    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    valor = models.FloatField()
    date = models.DateField()
    classificacao = models.CharField(
        max_length=3,
        choices=Classificacao.choices,
        default=Classificacao.GENERALIDADES,
    )

    def __str__(self):
        return self.nome
