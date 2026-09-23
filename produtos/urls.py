from . import views
from django.contrib import admin
from django.urls import path

urls = [
    path('home', views.home),
    path('editar/<int:id>', views.editar),
    path('excluir/<int:id>', views.excluir),
    path('dashboard', views.dashboard),
    path('produtos', views.produtos),
    path('entrada/<int:id>', views.entrada),
    path('saida/<int:id>', views.saida),
    path('carrinho', views.carrinho),
    path('carrinho/adicionar/<int:id>', views.adicionar_carrinho),
    path('carrinho/remover/<int:id>', views.remover_carrinho),
    path('carrinho/comprar', views.comprar),
]
