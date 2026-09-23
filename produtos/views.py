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

    repor_itens, repor_total = itens_da_lista(request, 'repor')
    retirar_itens, retirar_total = itens_da_lista(request, 'retirar')

    return render(request, 'produtos.html', {
        'produtos': Produto.objects.filter(filtro),
        'busca': busca,
        'tipo': tipo,
        'tipos': Produto.Tipo.choices,
        'repor_itens': repor_itens,
        'repor_total': repor_total,
        'retirar_itens': retirar_itens,
        'retirar_total': retirar_total,
        'painel': request.GET.get('painel'),
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

    for lista in ['repor', 'retirar']:
        itens = request.session.get(lista, {})
        itens.pop(str(id), None)
        request.session[lista] = itens

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


def itens_da_lista(request, lista):
    quantidades = request.session.get(lista, {})

    itens = []
    total = 0
    for produto in Produto.objects.filter(id__in=quantidades.keys()):
        quantidade = quantidades[str(produto.id)]
        subtotal = produto.valor * quantidade
        total += subtotal
        itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})

    return itens, total


def adicionar(request, lista, id):
    produto = Produto.objects.get(id=id)
    quantidade = int(request.POST.get('quantidade') or 0)

    itens = request.session.get(lista, {})
    na_lista = itens.get(str(id), 0)

    if quantidade < 1:
        messages.error(request, 'Escolha pelo menos 1 unidade.')
    elif lista == 'retirar' and na_lista + quantidade > produto.quantidade:
        messages.error(request, f'So tem {produto.quantidade} unidade(s) de {produto.nome} no estoque e voce ja separou {na_lista} para retirar.')
    else:
        itens[str(id)] = na_lista + quantidade
        request.session[lista] = itens
        messages.success(request, f'{quantidade} unidade(s) de {produto.nome} na lista.')

    return redirect(f'/produtos?painel={lista}')


def remover(request, lista, id):
    itens = request.session.get(lista, {})
    itens.pop(str(id), None)
    request.session[lista] = itens
    return redirect(f'/produtos?painel={lista}')


def confirmar(request, lista):
    itens = request.session.get(lista, {})

    if request.method != 'POST':
        return redirect('/produtos')

    if not itens:
        messages.error(request, 'A lista esta vazia.')
        return redirect(f'/produtos?painel={lista}')

    if lista == 'retirar':
        problemas = []
        for id, quantidade in itens.items():
            produto = Produto.objects.filter(id=id).first()

            if produto is None:
                problemas.append('Um produto da lista foi excluido do estoque.')
            elif quantidade > produto.quantidade:
                problemas.append(f'{produto.nome}: voce quer retirar {quantidade}, mas so tem {produto.quantidade} no estoque.')

        if problemas:
            for problema in problemas:
                messages.error(request, problema)
            return redirect(f'/produtos?painel={lista}')

    for id, quantidade in itens.items():
        produto = Produto.objects.filter(id=id).first()

        if produto is None:
            continue

        if lista == 'repor':
            produto.quantidade += quantidade
        else:
            produto.quantidade -= quantidade
        produto.save()

    request.session[lista] = {}

    if lista == 'repor':
        messages.success(request, 'Reposicao feita! O estoque foi atualizado.')
    else:
        messages.success(request, 'Retirada feita! O estoque foi atualizado.')

    return redirect(f'/produtos?painel={lista}')
