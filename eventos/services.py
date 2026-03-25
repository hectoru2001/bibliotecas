# eventos/services.py
from django.utils import timezone

# Import tardío para evitar import circular
def obtener_eventos_publicos(limit: int = 4):
    from .models import AgendaBiblioAprende, AgendaCultural

    items = []

    # DEBUG: cuenta en BD
    try:
        ba_count = AgendaBiblioAprende.objects.count()
        ac_count = AgendaCultural.objects.count()
        print("[SERVICES] BA count:", ba_count, "| AC count:", ac_count)
    except Exception as ex:
        print("[SERVICES] ERROR contando:", ex)

    def M(e, tipo):
        titulo = getattr(e, "titulo", getattr(e, "nombre", str(e)))
        fecha  = getattr(e, "fecha", getattr(e, "fecha_evento", None))
        hora_i = getattr(e, "hora", getattr(e, "hora_inicio", None))
        hora_f = getattr(e, "hora_fin", getattr(e, "hora_termino", None))
        hora = f"{hora_i} — {hora_f}" if (hora_i and hora_f) else (hora_i or hora_f)
        imagen = getattr(e, "imagen", getattr(e, "imagen_portada", None))
        link   = getattr(e, "link_registro", getattr(e, "url", None))
        return {
            "tipo": tipo,
            "titulo": titulo,
            "fecha": fecha,
            "hora": hora,
            "imagen": imagen,       # ImageField o string
            "link_registro": link,
        }

    # SIN FILTROS (solo ordena y limita)
    for e in AgendaBiblioAprende.objects.all():
        items.append(M(e, "biblio"))

    for e in AgendaCultural.objects.all():
        items.append(M(e, "cultural"))

    # Orden por fecha; None al final
    items.sort(key=lambda x: (x["fecha"] or timezone.datetime.max.date()))
    items = items[:limit]

    print("[SERVICES] Home items:", len(items))
    for i, it in enumerate(items, 1):
        print(f"[SERVICES] {i}.", it["titulo"], it["fecha"], it["hora"])

    return items
