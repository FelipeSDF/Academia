# Como listar os registros

## A view

```python
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})
```

O dicionario no final do `render` e o **contexto**: e a unica coisa que o template
enxerga. A chave (`'produtos'`) e o nome que voce vai usar no HTML.

## O template

```html
<ul>
    {% for produto in produtos %}
        <li>{{ produto.nome }} - {{ produto.marca }}</li>
    {% empty %}
        <li>Nenhum produto cadastrado.</li>
    {% endfor %}
</ul>
```

- **`{% empty %}`** roda quando a lista vem vazia. Evita a pagina ficar em branco.
- Todo `{% for %}` precisa de `{% endfor %}`.

## Formatando os valores

```html
{{ produto.valor|floatformat:2 }}      12.50
{{ produto.date|date:"d/m/Y" }}        23/09/2026
{{ produto.get_tipo_display }}         Alimento   (em vez de ALI)
```

O `|` e um **filtro**: transforma o valor antes de mostrar. O `:` passa um argumento.

`get_<campo>_display` so funciona em campo que tem `choices`. Sem ele aparece o
codigo cru que esta salvo no banco.

## Ordenando

```python
Produto.objects.all().order_by('nome')      # A -> Z
Produto.objects.all().order_by('-valor')    # maior -> menor (o menos inverte)
```

## Contando

```html
{{ produtos|length }} produtos cadastrados
```

## Erro classico

Se a lista aparece vazia mesmo tendo dados, quase sempre o nome no contexto
(`{'produtos': ...}`) esta diferente do nome no `{% for %}`. Eles tem que bater.
