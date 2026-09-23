from django import forms
from .models import Peso

class PesoForm(forms.ModelForm):
    class Meta:
        model = Peso
        fields = ['nome','valor','marca','date', 'tipo']
