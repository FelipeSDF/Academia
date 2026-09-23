from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForm


# Create your views here.
def home(request):
    busca = request.GET.get('busca')
    tipo = request.GET.get('tipo')

    filtro = Q()

    if busca:
        filtro &= Q(nome__icontains=busca)

    if tipo:
        filtro &= Q(tipo=tipo)

    produtos = Produto.objects.filter(filtro)

    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = ProdutoForm()

    return render(request, 'index.html', {
        'form': form,
        'produtos': produtos,
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
            return redirect('/home')

    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'editar.html', {'form': form})


def excluir(request, id):
    Produto.objects.get(id=id).delete()
    return redirect('/home')
