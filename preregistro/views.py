# preregistro/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PreRegistroForm
from .models import PreRegistro  # Add this import

def pre_registro(request):
    if request.method == 'POST':
        form = PreRegistroForm(request.POST)
        if form.is_valid():
            pre_registro = form.save()  # Guardamos el pre-registro
            messages.success(request, f'Pre-registro guardado con éxito. ID: {pre_registro.id}')
            return redirect('confirmacion_pre_registro', pre_registro_id=pre_registro.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            for field, errors in form.errors.items():
                messages.error(request, f"Error en {field}: {errors}")
            return render(request, 'public/credencial.html', {'form': form})
    else:
        return redirect('credencial')

def confirmacion_pre_registro(request, pre_registro_id):
    # Obtenemos el pre-registro recién creado
    pre_registro = PreRegistro.objects.get(id=pre_registro_id)
    return render(request, 'preregistro/confirmacion_pre_registro.html', {'pre_registro': pre_registro})

def credencial(request):
    form = PreRegistroForm()
    return render(request, 'bibliotecas/credencial.html', {'form': form})

