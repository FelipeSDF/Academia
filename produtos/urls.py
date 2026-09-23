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
    path('repor/adicionar/<int:id>', views.adicionar, {'lista': 'repor'}),
    path('repor/remover/<int:id>', views.remover, {'lista': 'repor'}),
    path('repor/confirmar', views.confirmar, {'lista': 'repor'}),
    path('retirar/adicionar/<int:id>', views.adicionar, {'lista': 'retirar'}),
    path('retirar/remover/<int:id>', views.remover, {'lista': 'retirar'}),
    path('retirar/confirmar', views.confirmar, {'lista': 'retirar'}),
]
