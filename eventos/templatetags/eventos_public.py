# projects/eventos/templatetags/eventos_public.py
from django import template
from django.utils import timezone
from datetime import time, datetime
from ..models import AgendaBiblioAprende, AgendaCultural

register = template.Library()

def _img_url(field):
    """Devuelve la URL del ImageField o None."""
    try:
        return field.url if field else None
    except Exception:
        return None

def _fmt_time(t):
    try:
        return t.strftime("%H:%M") if t else None
    except Exception:
        return None

@register.inclusion_tag("eventos/_home_cards.html")
def proximos_eventos_home(limit=4):

    hoy = timezone.localdate()
    items = []


    for e in AgendaBiblioAprende.objects.all():

        is_next = (not e.ya_finalizo()) if hasattr(e, "ya_finalizo") else (
            (e.fecha_fin and e.fecha_fin >= hoy) or (e.fecha and e.fecha >= hoy)
        )
        if not is_next:
            continue

        start_t = e.hora
        end_t   = e.hora_fin
        time_str = None
        if start_t and end_t:
            time_str = f"{_fmt_time(start_t)} — {_fmt_time(end_t)}"
        elif start_t:
            time_str = _fmt_time(start_t)

        items.append({
            "kind": "biblio",
            "title": e.nombre,
            "date":  e.fecha,
            "time_str": time_str,
            "time_sort": start_t or time.max, 
            "place": None,
            "img_url": _img_url(e.imagen),
            "link": None,  
        })


    for e in AgendaCultural.objects.all():
        if not e.fecha or e.fecha < hoy:
            continue
        items.append({
            "kind": "cultural",
            "title": e.nombre,
            "date":  e.fecha,
            "time_str": None,
            "time_sort": time.max,                   
            "place": None,
            "img_url": _img_url(e.imagen),
            "link": e.enlace or None,
        })


    if not items:
        for e in AgendaBiblioAprende.objects.all():
            items.append({
                "kind": "biblio",
                "title": e.nombre,
                "date":  e.fecha,
                "time_str": _fmt_time(e.hora) if e.hora else None,
                "time_sort": e.hora or time.max,
                "place": None,
                "img_url": _img_url(e.imagen),
                "link": None,
            })
        for e in AgendaCultural.objects.all():
            items.append({
                "kind": "cultural",
                "title": e.nombre,
                "date":  e.fecha,
                "time_str": None,
                "time_sort": time.max,
                "place": None,
                "img_url": _img_url(e.imagen),
                "link": e.enlace or None,
            })


    items.sort(key=lambda x: (
        x["date"] or datetime.max.date(),
        x["time_sort"] or time.max,
        x["title"].lower()
    ))

    return {"eventos": items[:limit]}
