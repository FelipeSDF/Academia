# Como pesquisar

E a listagem com `.filter()` no lugar do `.all()`.

## A view

```python
def home(request):
    busca = request.GET.get('busca')        # le da URL: /home?busca=arroz

    if busca:
        produtos = Produto.objects.filter(nome__icontains=busca)
    else:
        produtos = Produto.objects.all()

    return render(request, 'index.html', {'produtos': produtos, 'busca': busca})
```

## O template

```html
<form method='get'>
    <input type="text" name="busca" value="{{ busca|default_if_none:'' }}" placeholder="Pesquisar pelo nome">
    <button> pesquisar </button>
</form>
```

## Por que cada parte existe

- **`method='get'`** — a busca so le, nao muda o banco. Por isso vira parte da URL
  (`/home?busca=arroz`) e nao precisa de `{% csrf_token %}`. O form de cadastro e
  `post` porque grava.
- **`name="busca"`** no input e **`.get('busca')`** na view — essa string igual nos
  dois lugares e a unica ligacao entre o HTML e o Python. Se errar uma letra, nao funciona.
- **`if busca:`** — quando ninguem pesquisou, `.get()` devolve `None`; ai cai no
  `else` e mostra tudo.
- **`value="{{ busca }}"`** — faz o texto continuar escrito na caixa depois de
  pesquisar. Sem isso a caixa volta vazia e fica estranho.
- **`|default_if_none:''`** — sem ele, apareceria a palavra `None` dentro da caixa
  quando a pagina abre sem busca. Alternativa: usar `request.GET.get('busca', '')`
  na view, ai o segundo argumento ja e o padrao e o template fica so `{{ busca }}`.

## Tipos de filtro

O padrao e `campo__comparacao=valor`:

```python
nome__icontains='arr'      contem, ignorando maiuscula   -> LIKE %arr%
nome__contains='Hal'       contem, respeitando maiuscula
nome__exact='Arroz'       igual exato
nome__startswith='Arr'     comeca com
valor__gte=100             maior ou igual
valor__lte=100             menor ou igual
date__year=2026            ano da data
tipo='ALI'                 sem __ nenhum = igual
```

## Filtrando por mais de um campo

Virgula significa E:

```python
Produto.objects.filter(nome__icontains=busca, tipo='ALI')
```

Para OU, precisa do `Q`:

```python
from django.db.models import Q
Produto.objects.filter(Q(nome__icontains=busca) | Q(marca__icontains=busca))
```

## Busca em dois campos ao mesmo tempo

Util quando o usuario digita e nao sabe se e nome ou marca — use o `Q` acima.

## Juntando busca e ordenacao

```python
produtos = Produto.objects.filter(nome__icontains=busca).order_by('nome')
```

Pode encadear a vontade: o Django so vai no banco quando o resultado e usado.
