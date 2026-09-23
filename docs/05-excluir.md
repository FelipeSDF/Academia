# Como excluir um registro

## A view

```python
from django.shortcuts import redirect

def excluir(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('/home')
```

Tres linhas: acha, apaga, volta pra listagem.

## A rota

```python
path('excluir/<int:id>', views.excluir)
```

## O link

```html
<a href="/excluir/{{ produto.id }}">excluir</a>
```

## Por que o redirect

Sem ele a view nao devolve nada e da erro
(`didn't return an HttpResponse object`). Depois de apagar nao ha o que mostrar,
entao manda a pessoa de volta pra lista.

## Pedindo confirmacao (opcional)

Com um `confirm` do JavaScript, sem pagina nova:

```html
<a href="/excluir/{{ produto.id }}" onclick="return confirm('Excluir esse produto?')">excluir</a>
```

Ou com uma pagina de confirmacao, que e o jeito mais correto:

```python
def excluir(request, id):
    produto = Produto.objects.get(id=id)

    if request.method == 'POST':
        produto.delete()
        return redirect('/home')

    return render(request, 'confirmar.html', {'produto': produto})
```

```html
<p>Excluir {{ produto.nome }}?</p>
<form method='post'>
    {% csrf_token %}
    <button> sim, excluir </button>
</form>
```

Por que isso e melhor: apagar por link (`get`) significa que qualquer coisa que
abra a URL apaga o registro. Por `post`, so apaga quem clicou no botao de verdade.
