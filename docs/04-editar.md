# Como editar um registro

E o cadastro com uma palavra a mais: **`instance`**.

## A view

```python
from django.shortcuts import render, redirect

def editar(request, id):
    produto = Produto.objects.get(id=id)              # pega o registro pelo id da URL

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)    # sem instance criaria um NOVO
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = ProdutoForm(instance=produto)          # abre ja preenchido

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
<a href="/editar/{{ produto.id }}">editar</a>
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
| `ProdutoForm(request.POST)` | `ProdutoForm(request.POST, instance=produto)` |
| cria um registro novo | altera o registro existente |

`instance` no GET (`ProdutoForm(instance=produto)`) serve pra outra coisa: preencher os
campos com o que ja esta salvo, pra pessoa ver o que esta editando.

## Usando a mesma view pra criar e editar

Da pra fazer o `id` ser opcional:

```python
def salvar(request, id=None):
    produto = Produto.objects.get(id=id) if id else None
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('/home')
    return render(request, 'editar.html', {'form': form})
```

Mais curto, mas mais dificil de ler. Para a prova, duas views separadas e mais seguro.
