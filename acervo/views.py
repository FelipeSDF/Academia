from django.shortcuts import render
from .models import Livro
from .forms import LivroForm

# Create your views here.
def home(request):
    livros = Livro.objects.all()

    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        livros = Livro.objects.all()
        form = LivroForm()

    return render(request, 'index.html', {'form':form,'livros': livros})
