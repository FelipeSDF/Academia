# Como editar um registro

E o cadastro com uma palavra a mais: **`instance`**.

## A view

```python
from django.shortcuts import render, redirect

def editar(request, id):
    peso = Peso.objects.get(id=id)              # pega o registro pelo id da URL

    if request.method == 'POST':
        form = PesoForm(request.POST, instance=peso)    # sem instance criaria um NOVO
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = PesoForm(instance=peso)          # abre ja preenchido

    return render(request, 'editar.html', {'form': form})
```

## A rota

```python
path('editar/<int:id>', views.editar)
```

O `<int:id>` captura um numero da URL e entrega como argumento pra view. O nome
dentro dos `<>` tem que ser igual ao parametro da funcao (`def editar(request, id)`).

## O link na listagem

```html
<a href="/editar/{{ peso.id }}">editar</a>
```

Todo registro tem um `id` automatico, criado pelo Django. Voce nao declara no model.

## O template editar.html

Igual ao de cadastro:

```html
<form method='post'>
    {% csrf_token %}
    {{ form }}
    <button> salvar </button>
</form>
```

## A unica coisa pra decorar

| Sem instance | Com instance |
|---|---|
| `PesoForm(request.POST)` | `PesoForm(request.POST, instance=peso)` |
| cria um registro novo | altera o registro existente |

`instance` no GET (`PesoForm(instance=peso)`) serve pra outra coisa: preencher os
campos com o que ja esta salvo, pra pessoa ver o que esta editando.

## Usando a mesma view pra criar e editar

Da pra fazer o `id` ser opcional:

```python
def salvar(request, id=None):
    peso = Peso.objects.get(id=id) if id else None
    form = PesoForm(request.POST or None, instance=peso)
    if form.is_valid():
        form.save()
        return redirect('/home')
    return render(request, 'editar.html', {'form': form})
```

Mais curto, mas mais dificil de ler. Para a prova, duas views separadas e mais seguro.
