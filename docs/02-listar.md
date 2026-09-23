# Como listar os registros

## A view

```python
def home(request):
    pesos = Peso.objects.all()
    return render(request, 'index.html', {'pesos': pesos})
```

O dicionario no final do `render` e o **contexto**: e a unica coisa que o template
enxerga. A chave (`'pesos'`) e o nome que voce vai usar no HTML.

## O template

```html
<ul>
    {% for peso in pesos %}
        <li>{{ peso.nome }} - {{ peso.marca }}</li>
    {% empty %}
        <li>Nenhum peso cadastrado.</li>
    {% endfor %}
</ul>
```

- **`{% empty %}`** roda quando a lista vem vazia. Evita a pagina ficar em branco.
- Todo `{% for %}` precisa de `{% endfor %}`.

## Formatando os valores

```html
{{ peso.valor|floatformat:2 }}      12.50
{{ peso.date|date:"d/m/Y" }}        23/09/2026
{{ peso.get_tipo_display }}         Halter   (em vez de HAL)
```

O `|` e um **filtro**: transforma o valor antes de mostrar. O `:` passa um argumento.

`get_<campo>_display` so funciona em campo que tem `choices`. Sem ele aparece o
codigo cru que esta salvo no banco.

## Ordenando

```python
Peso.objects.all().order_by('nome')      # A -> Z
Peso.objects.all().order_by('-valor')    # maior -> menor (o menos inverte)
```

## Contando

```html
{{ pesos|length }} pesos cadastrados
```

## Erro classico

Se a lista aparece vazia mesmo tendo dados, quase sempre o nome no contexto
(`{'pesos': ...}`) esta diferente do nome no `{% for %}`. Eles tem que bater.
