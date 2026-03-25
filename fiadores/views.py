from django.shortcuts import render, redirect
from .forms import FiadorForm

def FiadorFormView(request):
    if request.method == 'POST':
        form = FiadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exitoso_fiador')
    else:
        form = FiadorForm()
    return render(request, 'fiadores/add_fiador.html', {'form': form})

def FiadorListView(request):
    return render(request, 'fiadores/exitoso_fiador.html')
