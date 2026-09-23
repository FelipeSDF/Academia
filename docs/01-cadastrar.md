# Como cadastrar um registro

## A view

```python
from django.shortcuts import render
from .models import Produto
from .forms import ProdutoForm

def home(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)      # form com os dados que chegaram
        if form.is_valid():
            form.save()                    # grava no banco
    else:
        form = ProdutoForm()                  # form vazio

    return render(request, 'index.html', {'form': form})
```

## O template

```html
<form method='post'>
    {% csrf_token %}
    {{ form }}
    <button> salvar </button>
</form>
```

## Por que cada parte existe

- **`request.method == 'POST'`** — a mesma view atende duas situacoes: abrir a pagina
  (GET, mostra o form vazio) e receber o envio (POST, salva). O `if` separa as duas.
- **`ProdutoForm(request.POST)`** — sem o `request.POST` dentro, o form nasce vazio e
  nao salva nada. Esse e o erro mais comum.
- **`form.is_valid()`** — valida os campos. Se estiver invalido, o form volta pro
  template ja com as mensagens de erro dentro dele.
- **`form.save()`** — como e um `ModelForm`, ele sabe em qual tabela gravar.
- **`{% csrf_token %}`** — obrigatorio em todo form `post`. Sem ele da erro 403.
- **`{{ form }}`** — desenha todos os campos de uma vez, com labels.

## Se quiser desenhar campo por campo

```html
{{ form.nome.label }} {{ form.nome }}
{{ form.valor.label }} {{ form.valor }}
```

## Limpar o form depois de salvar

Do jeito acima, os dados continuam na tela depois de salvar. Para limpar:

```python
if form.is_valid():
    form.save()
    form = ProdutoForm()       # troca por um vazio
```

Ou redirecionar (melhor, evita salvar duas vezes se o usuario der F5):

```python
from django.shortcuts import redirect

if form.is_valid():
    form.save()
    return redirect('/home')
```
