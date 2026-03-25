from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import VisitaForm
from .models import VisitaGuiada

def reservar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)

            fecha_visita = form.cleaned_data['fecha_visita']   # <-- date (no datetime)
            biblioteca   = form.cleaned_data['biblioteca']

            # ¿Ya hay una visita ese mismo día en esa biblioteca?
            ya_ocupada = VisitaGuiada.objects.filter(
                biblioteca=biblioteca,
                fecha_visita=fecha_visita         # <-- igualdad directa porque es DateField
            ).exists()

            if ya_ocupada:
                messages.error(request, 'Ya existe una visita programada ese día en esta biblioteca.')
                return render(request, 'public/visita.html', {'form': form})

            visita.save()

            fecha_disponible = timezone.localdate() + timedelta(days=7)
            fecha_disponible_formateada = fecha_disponible.strftime('%d/%m/%Y')

            return render(request, 'visita/confirmacion_visita.html', {
                'visita': visita,
                'confirmado': True,
                'fecha_disponible': fecha_disponible_formateada
            })
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            return render(request, 'public/visita.html', {'form': form})
    else:
        return redirect('visita')



def confirmacion_visita(request, visita_id):
    try:
        visita = VisitaGuiada.objects.get(id=visita_id)
        return render(request, 'visita/confirmacion_visita.html', {
            'visita': visita,
            'confirmado': True
        })
    except VisitaGuiada.DoesNotExist:
        messages.error(request, 'La visita no existe.')
        return redirect('visita')


def visita(request):
    form = VisitaForm()
    return render(request, 'public/visita.html', {'form': form})
