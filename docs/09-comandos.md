# Comandos

## Do dia a dia

```bash
python manage.py runserver          # sobe o servidor em 127.0.0.1:8000
python manage.py runserver 8080     # em outra porta
python manage.py makemigrations     # gera o arquivo de migracao depois de mexer no model
python manage.py migrate            # aplica no banco
python manage.py createsuperuser    # cria o login do /admin
python manage.py check              # procura erro de configuracao sem subir o servidor
```

Para parar o servidor: `Ctrl + C`.

## Comecando um projeto do zero

```bash
python -m venv venv
venv\Scripts\activate               # Windows
pip install django

django-admin startproject academia .    # o ponto evita criar pasta duplicada
python manage.py startapp pesos
```

Depois do `startapp`, registre o app no `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'pesos',
]
```

Esquecer isso e a causa numero 1 de `TemplateDoesNotExist`.

## Rodando este projeto

```bash
venv\Scripts\activate
python manage.py migrate            # cria o banco, que nao vem no repositorio
python manage.py runserver
```

Abre em http://127.0.0.1:8000/home

## Ambiente virtual

```bash
python -m venv venv                 # cria
venv\Scripts\activate               # ativa (aparece (venv) no terminal)
deactivate                          # sai
pip freeze > requirements.txt       # salva a lista de pacotes
pip install -r requirements.txt     # instala a lista em outra maquina
```

## Migracoes quando da errado

```bash
python manage.py showmigrations                 # ve o que ja foi aplicado
python manage.py makemigrations pesos           # so de um app
python manage.py migrate pesos 0001             # volta pra uma migracao anterior
```

Em projeto de estudo, quando o banco embola de vez, o caminho rapido e apagar o
`db.sqlite3` e os arquivos numerados de `pesos/migrations/` (menos o `__init__.py`)
e rodar `makemigrations` + `migrate` de novo. Isso **apaga todos os dados** — so
faca em projeto de aula.

## Shell (testar consultas sem navegador)

```bash
python manage.py shell
```

```python
from pesos.models import Peso
Peso.objects.all()
Peso.objects.filter(nome__icontains='hal')
Peso.objects.create(nome='Halter 10kg', marca='X', valor=90, date='2026-09-23', tipo='HAL')
```

Otimo pra conferir se o filtro que voce escreveu na view devolve o que voce espera.
