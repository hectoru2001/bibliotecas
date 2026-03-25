from django.shortcuts import render, redirect
from .forms import AgendaBiblioAprendeForm, AgendaCulturalForm
from .models import AgendaBiblioAprende, AgendaCultural
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from typing import List, Dict
from django.utils import timezone


def es_admin_eventos(user):
    return user.groups.filter(name='AdministradoresEventos').exists()

# @user_passes_test(es_admin_eventos)
def crear_biblioaprende(request):
    form = AgendaBiblioAprendeForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, ' Evento guardado correctamente.')
            form = AgendaBiblioAprendeForm() 
        else:
            messages.error(request, ' Ocurrió un error al guardar el evento.')

    return render(request, 'eventos/crear_biblioaprende.html', {'form': form})


def crear_agenda_cultural(request):
    if request.method == 'POST':
        form = AgendaCulturalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ' El evento de agenda cultural se guardó correctamente.')
            form = AgendaCulturalForm()
        else:
            messages.error(request, ' Ocurrió un error al guardar el evento.')
    else:
        form = AgendaCulturalForm()
    return render(request, 'eventos/crear_agenda_cultural.html', {'form': form})


def lista_biblioaprende(request):
    eventos = AgendaBiblioAprende.objects.all()
    eventos_vigentes = [e for e in eventos if not e.ya_finalizo()]
    eventos_vigentes.sort(key=lambda e: (e.fecha, e.hora))  # ordenar por fecha y hora
    return render(request, 'eventos/lista_biblioaprende.html', {'eventos': eventos_vigentes})


def agenda_cultural(request):
    eventos = AgendaCultural.objects.all()  # si tienes un modelo AgendaCultural
    return render(request, 'eventos/agenda_cultural.html', {'eventos': eventos})

def event_list(request):
    """
    Muestra en una sola tabla todos los eventos (BiblioAprende + AgendaCultural),
    con acciones para Editar/Eliminar.
    Soporta búsqueda simple por título y paginación.
    """
    q = (request.GET.get('q') or '').strip()

    # Trae y normaliza ambos tipos de eventos a una lista de dicts homogénea
    items = []
    for e in AgendaBiblioAprende.objects.all():
        titulo = getattr(e, 'titulo', getattr(e, 'nombre', str(e)))
        if q and q.lower() not in str(titulo).lower():
            continue
        items.append({
            'pk': e.pk,
            'tipo': 'biblio',
            'titulo': titulo,
            'fecha': getattr(e, 'fecha', None),
            'hora': getattr(e, 'hora', None),
            'estado': 'Finalizado' if hasattr(e, 'ya_finalizo') and e.ya_finalizo() else 'Próximo',
            'edit_url': reverse('editar_biblioaprende', args=[e.pk]),
            'delete_url': reverse('eliminar_biblioaprende', args=[e.pk]),
        })

    for e in AgendaCultural.objects.all():
        titulo = getattr(e, 'titulo', getattr(e, 'nombre', str(e)))
        if q and q.lower() not in str(titulo).lower():
            continue
        items.append({
            'pk': e.pk,
            'tipo': 'cultural',
            'titulo': titulo,
            'fecha': getattr(e, 'fecha', None),
            'hora': getattr(e, 'hora', None),
            'estado': 'Finalizado' if hasattr(e, 'ya_finalizo') and e.ya_finalizo() else 'Próximo',
            'edit_url': reverse('editar_agenda_cultural', args=[e.pk]),
            'delete_url': reverse('eliminar_agenda_cultural', args=[e.pk]),
        })

    # Orden: fecha, hora (None al final)
    items.sort(key=lambda x: (
        x['fecha'] or timezone.datetime.max.replace(tzinfo=timezone.utc),
        x['hora'] or timezone.datetime.max.time()
    ))

    paginator = Paginator(items, 20)  # 20 por página (ajústalo si quieres)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'eventos/event_list.html', {
        'page_obj': page_obj,
        'q': q,
    })


def editar_biblioaprende(request, pk):
    evento = get_object_or_404(AgendaBiblioAprende, pk=pk)
    form = AgendaBiblioAprendeForm(request.POST or None, request.FILES or None, instance=evento)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, ' Evento BiblioAprende actualizado.')
            return redirect('event_list')
        messages.error(request, ' Revisa el formulario.')
    return render(request, 'eventos/editar_biblioaprende.html', {'form': form, 'evento': evento})

def eliminar_biblioaprende(request, pk):
    if request.method != 'POST':
        messages.error(request, 'Operación no permitida.')
        return redirect('event_list')
    evento = get_object_or_404(AgendaBiblioAprende, pk=pk)
    evento.delete()
    messages.success(request, ' Evento BiblioAprende eliminado.')
    return redirect('event_list')


def editar_agenda_cultural(request, pk):
    evento = get_object_or_404(AgendaCultural, pk=pk)
    form = AgendaCulturalForm(request.POST or None, request.FILES or None, instance=evento)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, ' Evento de Agenda Cultural actualizado.')
            return redirect('event_list')
        messages.error(request, ' Revisa el formulario.')
    return render(request, 'eventos/editar_agenda_cultural.html', {'form': form, 'evento': evento})

def eliminar_agenda_cultural(request, pk):
    if request.method != 'POST':
        messages.error(request, 'Operación no permitida.')
        return redirect('event_list')
    evento = get_object_or_404(AgendaCultural, pk=pk)
    evento.delete()
    messages.success(request, ' Evento de Agenda Cultural eliminado.')
    return redirect('event_list')

