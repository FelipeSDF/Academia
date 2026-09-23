from django.shortcuts import render
from .models import Produto
from .forms import ProdutoForm


# Create your views here.
def home(request):
    busca = request.GET.get('busca')

    if busca:
        produtos = Produto.objects.filter(nome__icontains=busca)
    else:
        produtos = Produto.objects.all()

    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = ProdutoForm()

    return render(request, 'index.html', {'form':form,'produtos': produtos,'busca': busca})
