# Como excluir um registro

## A view

```python
from django.shortcuts import redirect

def excluir(request, id):
    peso = Peso.objects.get(id=id)
    peso.delete()
    return redirect('/home')
```

Tres linhas: acha, apaga, volta pra listagem.

## A rota

```python
path('excluir/<int:id>', views.excluir)
```

## O link

```html
<a href="/excluir/{{ peso.id }}">excluir</a>
```

## Por que o redirect

Sem ele a view nao devolve nada e da erro
(`didn't return an HttpResponse object`). Depois de apagar nao ha o que mostrar,
entao manda a pessoa de volta pra lista.

## Pedindo confirmacao (opcional)

Com um `confirm` do JavaScript, sem pagina nova:

```html
<a href="/excluir/{{ peso.id }}" onclick="return confirm('Excluir esse peso?')">excluir</a>
```

Ou com uma pagina de confirmacao, que e o jeito mais correto:

```python
def excluir(request, id):
    peso = Peso.objects.get(id=id)

    if request.method == 'POST':
        peso.delete()
        return redirect('/home')

    return render(request, 'confirmar.html', {'peso': peso})
```

```html
<p>Excluir {{ peso.nome }}?</p>
<form method='post'>
    {% csrf_token %}
    <button> sim, excluir </button>
</form>
```

Por que isso e melhor: apagar por link (`get`) significa que qualquer coisa que
abra a URL apaga o registro. Por `post`, so apaga quem clicou no botao de verdade.
