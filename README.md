# Academia

Projeto Django simples para cadastro de pesos de uma academia. Feito para a prova de Django.

## O que faz

- Cadastra um peso (nome, marca, valor, data e tipo)
- Lista todos os pesos cadastrados
- Pesquisa pelo nome

## Estrutura

```
academia/          configuracoes do projeto (settings, urls)
pesos/             app principal
  models.py        model Peso
  forms.py         PesoForm (ModelForm)
  views.py         view home (cadastro + listagem + busca)
  urls.py          rota /home
  templates/
    index.html     a unica pagina
manage.py
```

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate
pip install django

python manage.py migrate
python manage.py runserver
```

Depois abra http://127.0.0.1:8000/home

O banco (`db.sqlite3`) nao vai para o repositorio, entao o `migrate` cria um novo na primeira vez.

## Admin

```bash
python manage.py createsuperuser
```

Disponivel em http://127.0.0.1:8000/admin/

## Model

| Campo | Tipo | Observacao |
|-------|------|------------|
| nome  | CharField | nome do peso |
| marca | CharField | fabricante |
| valor | FloatField | preco |
| date  | DateField | data de compra |
| tipo  | CharField | choices: Halter, Anilha, Barra, Kettlebell, Caneleira |
