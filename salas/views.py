from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SalaForm
from .models import ReservaSala
from visita.models import VisitaGuiada
from django.utils.timezone import make_aware
from datetime import datetime, timedelta, timezone

def reservar_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            fecha_reserva = form.cleaned_data['fecha_reserva']
            biblioteca = form.cleaned_data['biblioteca']

            fecha_inicio = fecha_reserva.replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = fecha_reserva.replace(hour=23, minute=59, second=59, microsecond=999999)


            fecha_disponible = datetime.now() + timedelta(days=7)
            fecha_disponible_formateada = fecha_disponible.strftime('%d/%m/%Y')

            visitas = VisitaGuiada.objects.filter(
                fecha_visita__range=(fecha_inicio, fecha_fin),
                biblioteca=biblioteca
            )

            if visitas.exists():
                messages.error(request, 'Ya existe una visita programada ese dia en esta biblioteca.')
                return render(request, 'public/salas.html', {'form': form})

            return render(request, 'salas/confirmacion_sala.html', {
                'form': form,
                'preconfirmacion': True,
                'fecha_disponible': fecha_disponible_formateada,
            })
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            return render(request, 'public/salas.html', {'form': form})
    else:
        return redirect('salas')
    
def salas(request):
    form = SalaForm()
    return render(request, 'public/salas.html', {'form': form})

def confirmar_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            salas = form.save()
            return render(request, 'salas/confirmacion_sala.html', {'sala': salas, 'confirmado': True})
        else:
            messages.error(request, 'Error al confirmar la reserva.')
            return redirect('salas')
    return redirect('salas')

