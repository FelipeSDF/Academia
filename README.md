# Estoque

Projeto Django simples para controle de estoque de produtos. Feito para a prova de Django.

## O que faz

- **Cadastro** (`/home`): cadastra um produto (nome, valor, quantidade, marca, data, tipo e link da imagem)
- **Produtos** (`/produtos`): mostra os produtos em cards, com busca pelo nome e filtro por tipo.
  Cada card tem os botoes + e - para entrada e saida do estoque (o - nao deixa a quantidade ficar negativa),
  e os links de editar e excluir
- **Dashboard** (`/dashboard`): resumo dos precos e graficos de produtos por categoria

## Estrutura

```
estoque/             configuracoes do projeto (settings, urls)
produtos/            app principal
  models.py          model Produto
  forms.py           ProdutoForm (ModelForm) com a validacao do valor
  views.py           cadastro, listagem, editar, excluir, entrada, saida e dashboard
  urls.py            rotas
  fixtures/
    produtos.json    produtos de exemplo
  templates/
    cadastro.html
    produtos.html
    editar.html
    dashboard.html
manage.py
```

## Como rodar

Precisa do Python 3.12 ou mais novo.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata produtos
python manage.py runserver
```

No Linux/Mac o segundo comando e `source venv/bin/activate`.

Depois abra http://127.0.0.1:8000/home

O banco (`db.sqlite3`) nao vai para o repositorio, entao o `migrate` cria um novo na primeira vez
e o `loaddata` coloca os produtos de exemplo nele.

Os graficos do dashboard usam o Chart.js pela internet, entao precisam de conexao para aparecer.
As imagens dos produtos tambem sao links da internet.

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
| valor | FloatField | preco, tem que ser maior que zero |
| quantidade | PositiveIntegerField | quantidade em estoque |
| date  | DateField | data de entrada |
| tipo  | CharField | choices: Alimento, Bebida, Limpeza, Higiene, Papelaria |
| imagem | URLField | link da imagem, opcional |
