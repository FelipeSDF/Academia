from django.shortcuts import render
from .models import Peso
from .forms import PesoForm


# Create your views here.
def home(request):
    busca = request.GET.get('busca')

    if busca:
        pesos = Peso.objects.filter(nome__icontains=busca)
    else:
        pesos = Peso.objects.all()

    if request.method == 'POST':
        form = PesoForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = PesoForm()

    return render(request, 'index.html', {'form':form,'pesos': pesos,'busca': busca})
