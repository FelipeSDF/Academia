from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','valor','quantidade','marca','date', 'tipo', 'imagem']
        labels = {'date': 'Data de entrada', 'imagem': 'Link da imagem'}
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')

        if valor <= 0:
            raise forms.ValidationError("O valor do produto deve ser maior que zero.")

        return valor
