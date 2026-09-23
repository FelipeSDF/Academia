# Estoque

Projeto Django simples para cadastro de produtos de um estoque. Feito para a prova de Django.

## O que faz

- Cadastra um produto (nome, marca, valor, data e tipo)
- Lista todos os produtos cadastrados
- Pesquisa pelo nome

## Estrutura

```
estoque/           configuracoes do projeto (settings, urls)
produtos/          app principal
  models.py        model Produto
  forms.py         ProdutoForm (ModelForm)
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
| nome  | CharField | nome do produto |
| marca | CharField | fabricante |
| valor | FloatField | preco |
| date  | DateField | data de entrada |
| tipo  | CharField | choices: Alimento, Bebida, Limpeza, Higiene, Papelaria |
