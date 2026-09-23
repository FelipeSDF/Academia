# Como ligar uma view a uma rota

Sao dois arquivos: o do app e o do projeto.

## 1. No app (`produtos/urls.py`)

```python
from . import views
from django.urls import path

urls = [
    path('home', views.home),
    path('editar/<int:id>', views.editar),
    path('excluir/<int:id>', views.excluir),
]
```

## 2. No projeto (`estoque/urls.py`)

```python
from django.contrib import admin
from django.urls import path
from produtos import urls as produtosViews

urlpatterns = [
    path('admin/', admin.site.urls),
] + produtosViews.urls
```

Aqui a lista do app e somada na lista do projeto. Esse e o jeito que este projeto
usa. O jeito mais comum na documentacao e com `include`:

```python
# no projeto
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produtos.urls')),
]

# no app, a lista precisa se chamar urlpatterns
urlpatterns = [
    path('home', views.home),
]
```

Os dois funcionam. Nao misture.

## Passando valor pela URL

```python
path('editar/<int:id>', views.editar)
```

```python
def editar(request, id):     # o nome tem que ser igual ao de dentro dos <>
```

Tipos: `<int:id>` numero, `<str:nome>` texto, `<slug:slug>` texto-com-hifen.

## Dando nome pra rota

```python
path('home', views.home, name='home')
```

Ai no template voce usa o nome em vez do caminho:

```html
<a href="{% url 'home' %}">inicio</a>
<a href="{% url 'editar' produto.id %}">editar</a>
```

Vantagem: se um dia mudar o caminho de `/home` pra `/inicio`, os links continuam
funcionando. Se usar `{% url %}` sem ter posto `name=`, da `NoReverseMatch`.

## A rota vazia (pagina inicial)

```python
path('', views.home)        # responde em http://127.0.0.1:8000/
```
