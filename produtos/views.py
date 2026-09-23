from django.db.models import Q, Avg
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/produtos')

    else:
        form = ProdutoForm()

    return render(request, 'cadastro.html', {'form': form})


def produtos(request):
    busca = request.GET.get('busca')
    tipo = request.GET.get('tipo')

    filtro = Q()

    if busca:
        filtro &= Q(nome__icontains=busca)

    if tipo:
        filtro &= Q(tipo=tipo)

    return render(request, 'produtos.html', {
        'produtos': Produto.objects.filter(filtro),
        'busca': busca,
        'tipo': tipo,
        'tipos': Produto.Tipo.choices,
    })


def editar(request, id):
    produto = Produto.objects.get(id=id)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()
            return redirect('/produtos')

    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'editar.html', {'form': form})


def excluir(request, id):
    Produto.objects.get(id=id).delete()

    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(id), None)
    request.session['carrinho'] = carrinho

    return redirect('/produtos')


def dashboard(request):
    produtos = Produto.objects.all()

    categorias = []
    for valor, nome in Produto.Tipo.choices:
        da_categoria = produtos.filter(tipo=valor)
        categorias.append({
            'nome': nome,
            'unidades': sum(p.quantidade for p in da_categoria),
            'valor': round(sum(p.valor * p.quantidade for p in da_categoria), 2),
        })

    return render(request, 'dashboard.html', {
        'total': produtos.count(),
        'unidades': sum(p.quantidade for p in produtos),
        'valor_estoque': sum(p.valor * p.quantidade for p in produtos),
        'preco_medio': produtos.aggregate(media=Avg('valor'))['media'] or 0,
        'sem_estoque': produtos.filter(quantidade=0).count(),
        'repor': produtos.filter(quantidade__lte=5).order_by('quantidade'),
        'categorias': categorias,
    })


def entrada(request, id):
    produto = Produto.objects.get(id=id)
    produto.quantidade += 1
    produto.save()
    return redirect('/produtos')


def saida(request, id):
    produto = Produto.objects.get(id=id)

    if produto.quantidade > 0:
        produto.quantidade -= 1
        produto.save()

    return redirect('/produtos')


def adicionar_carrinho(request, id):
    produto = Produto.objects.get(id=id)
    quantidade = int(request.POST.get('quantidade') or 0)

    carrinho = request.session.get('carrinho', {})
    no_carrinho = carrinho.get(str(id), 0)

    if quantidade < 1:
        messages.error(request, 'Escolha pelo menos 1 unidade.')
    elif no_carrinho + quantidade > produto.quantidade:
        messages.error(request, f'So tem {produto.quantidade} unidade(s) de {produto.nome} no estoque e voce ja tem {no_carrinho} no carrinho.')
    else:
        carrinho[str(id)] = no_carrinho + quantidade
        request.session['carrinho'] = carrinho
        messages.success(request, f'{quantidade} unidade(s) de {produto.nome} no carrinho.')

    return redirect('/produtos')


def remover_carrinho(request, id):
    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(id), None)
    request.session['carrinho'] = carrinho
    return redirect('/carrinho')


def carrinho(request):
    carrinho = request.session.get('carrinho', {})

    itens = []
    total = 0
    for produto in Produto.objects.filter(id__in=carrinho.keys()):
        quantidade = carrinho[str(produto.id)]
        subtotal = produto.valor * quantidade
        total += subtotal
        itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})

    return render(request, 'carrinho.html', {'itens': itens, 'total': total})


def comprar(request):
    carrinho = request.session.get('carrinho', {})

    if request.method != 'POST':
        return redirect('/carrinho')

    if not carrinho:
        messages.error(request, 'O carrinho esta vazio.')
        return redirect('/carrinho')

    problemas = []
    for id, quantidade in carrinho.items():
        produto = Produto.objects.filter(id=id).first()

        if produto is None:
            problemas.append('Um produto do carrinho foi excluido do estoque.')
        elif quantidade > produto.quantidade:
            problemas.append(f'{produto.nome}: voce quer {quantidade}, mas so tem {produto.quantidade} no estoque.')

    if problemas:
        for problema in problemas:
            messages.error(request, problema)
        return redirect('/carrinho')

    for id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=id)
        produto.quantidade -= quantidade
        produto.save()

    request.session['carrinho'] = {}
    messages.success(request, 'Compra finalizada! O estoque foi atualizado.')
    return redirect('/carrinho')
