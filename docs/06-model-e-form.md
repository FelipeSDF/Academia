# Como criar o model e o form

## O model (`produtos/models.py`)

```python
from django.db import models

class Produto(models.Model):
    class Tipo(models.TextChoices):
        ALIMENTO = 'ALI', 'Alimento'      # valor no banco, texto na tela
        BEBIDA = 'BEB', 'Bebida'
        LIMPEZA = 'LIM', 'Limpeza'

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
        return self.nome         # como o registro aparece no admin e no shell
```

Cada classe e uma tabela. Cada atributo e uma coluna. O `id` o Django cria sozinho.

## Campos mais usados

```python
models.CharField(max_length=100)     texto curto (max_length e obrigatorio)
models.TextField()                   texto longo
models.IntegerField()                numero inteiro
models.FloatField()                  numero com virgula
models.DecimalField(max_digits=8, decimal_places=2)   dinheiro (mais correto)
models.DateField()                   data
models.DateTimeField()               data + hora
models.BooleanField()                sim/nao
models.EmailField()                  texto com validacao de email
models.ImageField(upload_to='fotos/')  imagem
```

Argumentos que servem em qualquer campo:

```python
null=True        aceita vazio no banco
blank=True       aceita vazio no formulario
default='x'      valor inicial
choices=...      lista fechada de opcoes
verbose_name=''  nome que aparece na label
```

## Choices

`TextChoices` faz o campo virar um `<select>` no form automaticamente.

```python
ALIMENTO = 'ALI', 'Alimento'
#         ^^^^^  ^^^^^^^^
#         banco   tela
```

No template, para mostrar o texto bonito:

```html
{{ produto.get_tipo_display }}     Alimento
{{ produto.tipo }}                 ALI
```

## Depois de mexer no model, SEMPRE

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` escreve o arquivo com as instrucoes. `migrate` executa no banco.
Esquecer isso da o erro `no such table` ou `no such column`.

## O form (`produtos/forms.py`)

```python
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'valor', 'marca', 'date', 'tipo']
```

`ModelForm` le o model e monta os campos sozinho — nao precisa redeclarar nada.

- `fields = '__all__'` inclui todos
- `exclude = ['date']` inclui todos menos esses
- A ordem da lista e a ordem na tela

## Deixando o campo de data com calendario

Por padrao o `DateField` vira uma caixa de texto onde a pessoa tem que digitar
`2026-09-23`. Para virar um seletor de data do navegador:

```python
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'valor', 'marca', 'date', 'tipo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
```

`widgets` troca o HTML que o campo gera. Da pra usar o mesmo truque pra colocar
classe de CSS ou placeholder:

```python
widgets = {
    'nome': forms.TextInput(attrs={'placeholder': 'Ex: Arroz 5kg', 'class': 'input'}),
}
```

## Registrando no admin (`produtos/admin.py`)

```python
from django.contrib import admin
from produtos.models import Produto

admin.site.register(Produto)
```

Sem essa linha o model nao aparece em `/admin/`.
