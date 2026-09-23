# Erros comuns

| Erro na tela | Causa mais provavel | Conserto |
|---|---|---|
| `TemplateDoesNotExist` | app fora do `INSTALLED_APPS`, ou template fora de `app/templates/` | registrar o app / mover o arquivo |
| `CSRF verification failed` | faltou `{% csrf_token %}` num form `post` | por a tag dentro do `<form>` |
| `no such table: pesos_peso` | faltou rodar as migracoes | `makemigrations` + `migrate` |
| `no such column` | mexeu no model e nao migrou | `makemigrations` + `migrate` |
| `NoReverseMatch` | usou `{% url 'x' %}` sem `name='x'` na rota | por o `name=` no `path()` |
| `didn't return an HttpResponse` | a view nao tem `return render(...)` ou `redirect(...)` | devolver alguma resposta |
| `Peso matching query does not exist` | `.get(id=...)` com id que nao existe | conferir o link, ou usar `get_object_or_404` |
| `Page not found (404)` | a URL digitada nao bate com nenhum `path()` | conferir `urls.py` (este projeto usa `/home`, sem barra no fim) |
| `Port is already in use` | ja tem um servidor rodando | `Ctrl+C` no outro terminal, ou `runserver 8080` |

## Erros que nao mostram erro nenhum

Esses sao os piores, porque a pagina abre normal e so nao faz o que deveria.

**O form nao salva e nao reclama**

Quase sempre e o `request.POST` que faltou:

```python
form = PesoForm()               # errado — nasce vazio, is_valid() da False
form = PesoForm(request.POST)   # certo
```

Se ainda assim nao salvar, e porque falta o `.save()` dentro do `if form.is_valid():`,
ou os dados estao invalidos. Para ver o motivo:

```python
print(form.errors)
```

Aparece no terminal onde o `runserver` esta rodando.

**A lista aparece vazia mesmo tendo dados**

O nome no contexto esta diferente do nome no `{% for %}`:

```python
return render(request, 'index.html', {'pesos': pesos})
```

```html
{% for peso in pesos %}      <- tem que ser 'pesos', igual a chave
```

**O choice mostra codigo em vez do texto**

```html
{{ peso.tipo }}                 HAL
{{ peso.get_tipo_display }}     Halter   <- este
```

**O CSS nao carrega**

Faltou `{% load static %}` na primeira linha do template, ou o caminho dentro do
`{% static %}` esta errado. Confira tambem se o arquivo esta em `app/static/app/`.

**Mudei o CSS e nao muda nada**

Cache do navegador. `Ctrl + F5`.

## Como ler um erro do Django

A pagina amarela de erro tem tudo. Duas coisas resolvem 90%:

1. A **primeira linha em negrito** no topo diz o que aconteceu
2. No meio da pilha, procure a linha que aponta pro **seu** arquivo
   (`pesos/views.py`), nao pros arquivos de dentro do `django/`. O erro esta la.
