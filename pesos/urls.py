from . import views
from django.contrib import admin
from django.urls import path

urls = [
    path('home', views.home)
]