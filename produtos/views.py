from django.db.models import Q, Avg
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
