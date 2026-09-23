# Como colocar CSS (arquivos estaticos)

Hoje o CSS deste projeto esta dentro de uma tag `<style>` no proprio `index.html`.
Funciona, mas o certo e por num arquivo `.css` separado. Isso e um **arquivo estatico**
(static file): CSS, JavaScript, imagens, fontes — tudo que o navegador baixa pronto,
sem o Django gerar nada.

## 1. Criar a pasta

Dentro do app, seguindo o padrao `app/static/app/`:

```
produtos/
  static/
    produtos/
      style.css
```

Por que repetir o nome do app: todos os apps jogam os estaticos no mesmo lugar no
final. Se dois apps tiverem um `style.css` solto, um sobrescreve o outro. A subpasta
com o nome do app evita a colisao.

## 2. Usar no template

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'produtos/style.css' %}">
</head>
```

- **`{% load static %}`** vai na **primeira linha** do arquivo, antes do `<!DOCTYPE>`
- **`{% static '...' %}`** monta a URL certa. Nunca escreva o caminho na mao.

## 3. Conferir o settings.py

Ja vem assim por padrao:

```python
STATIC_URL = 'static/'
```

E o `django.contrib.staticfiles` precisa estar no `INSTALLED_APPS` (tambem ja vem).

Com isso **em desenvolvimento ja funciona**: `runserver` acha os arquivos sozinho.

---

## E o collectstatic?

`collectstatic` **nao e necessario pra desenvolver**. Ele existe pra producao.

Em desenvolvimento (`DEBUG = True`), o `runserver` sai procurando os estaticos em
cada app, um por um, na hora do pedido. Isso e lento e o servidor de verdade
(nginx, Apache) nao sabe fazer isso. Entao, antes de publicar, voce roda um comando
que **copia todos os estaticos de todos os apps pra uma pasta unica**:

```python
# settings.py
import os

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # pasta de destino
```

```bash
python manage.py collectstatic
```

Resultado:

```
staticfiles/            <- criada pelo comando, e so copia
  admin/                <- o CSS do admin do Django veio junto
  produtos/
    style.css
```

Regras pra nao se perder:

- `STATIC_ROOT` e **destino**, nunca onde voce escreve. Nao edite nada la dentro —
  o proximo `collectstatic` sobrescreve.
- `STATIC_ROOT` nao pode ser igual a nenhuma pasta `static/` sua, senao da erro.
- A pasta `staticfiles/` vai pro `.gitignore` — e gerada, nao e codigo.
- Rode de novo toda vez que mudar um CSS em producao.

## STATICFILES_DIRS (estaticos fora dos apps)

Se quiser uma pasta `static/` na raiz do projeto, valendo pro site inteiro em vez de
um app so:

```python
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

O `collectstatic` tambem recolhe dessas pastas.

## Resumo dos tres nomes parecidos

| Nome | O que e |
|---|---|
| `STATIC_URL` | o prefixo na URL: `/static/produtos/style.css` |
| `STATICFILES_DIRS` | pastas extras **de onde ler**, fora dos apps |
| `STATIC_ROOT` | pasta unica **pra onde copiar**, so usada pelo collectstatic |

## Imagem no template

```html
<img src="{% static 'produtos/logo.png' %}" alt="logo">
```

Mesma coisa: `{% load static %}` no topo e `{% static %}` no caminho.

> Cuidado: `static` (CSS/JS/imagens do site) e diferente de `media` (arquivos que
> o usuario envia por upload). `MEDIA_URL`/`MEDIA_ROOT` sao outra configuracao e o
> `collectstatic` nao mexe neles.
