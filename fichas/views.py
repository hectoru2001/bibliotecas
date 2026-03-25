import csv
import subprocess
import tempfile
import os
from datetime import datetime

from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from .models import Ficha


# =========================
# Helpers
# =========================

def to_int(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def safe_parse_datetime(valor):
    if valor in (None, '', 'NULL'):
        return None

    if isinstance(valor, datetime):
        return valor

    valor = str(valor).strip()

    dt = parse_datetime(valor)
    if dt:
        return dt

    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]

    for f in formatos:
        try:
            return datetime.strptime(valor, f)
        except ValueError:
            pass

    return None


def obtener_tabla_access(ruta):
    try:
        tablas = subprocess.check_output(
            ["mdb-tables", "-1", ruta],
            stderr=subprocess.STDOUT
        ).decode("utf-8").splitlines()

        return tablas[0] if tablas else None

    except subprocess.CalledProcessError:
        return None


def leer_access(ruta, tabla):
    proceso = subprocess.Popen(
        ["mdb-export", ruta, tabla],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    lector = csv.DictReader(proceso.stdout)

    for fila in lector:
        yield fila

    proceso.stdout.close()
    proceso.wait()


# =========================
# View principal
# =========================

def importar_fichas(request):

    context = {}

    if request.method == "POST" and request.FILES.get("archivo"):

        archivo = request.FILES["archivo"]
        ruta_tmp = None

        total = 0
        errores = 0

        try:
            # Guardar archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mdb") as tmp:
                for chunk in archivo.chunks():
                    tmp.write(chunk)
                ruta_tmp = tmp.name

            # Obtener tabla
            tabla = obtener_tabla_access(ruta_tmp)

            if not tabla:
                context["error"] = "No se encontró ninguna tabla en el archivo"
                return render(request, "cargar_fichas.html", context)

            # Procesar archivo en streaming
            for fila in leer_access(ruta_tmp, tabla):

                ficha_no = to_int(fila.get("Ficha_No"))

                if not ficha_no:
                    errores += 1
                    continue

                try:
                    Ficha.objects.update_or_create(
                        ficha_no=ficha_no,
                        defaults={
                            "fecha": safe_parse_datetime(fila.get("Fecha")),
                            "fechamod": safe_parse_datetime(fila.get("FechaMod")),
                            "datosfijos": fila.get("DatosFijos"),
                            "etiquetasmar": fila.get("EtiquetasMARC"),
                            "tipomaterial": to_int(fila.get("TipoMaterial")) or 0,
                            "isbn": fila.get("ISBN"),
                            "titulo": fila.get("Titulo"),
                            "autor": fila.get("Autor"),
                            "clasificacion": fila.get("Clasificacion"),
                        }
                    )

                    total += 1

                except Exception:
                    errores += 1

        except Exception as e:
            context["error"] = str(e)

        finally:
            if ruta_tmp and os.path.exists(ruta_tmp):
                os.remove(ruta_tmp)

        context["cantidad"] = total
        context["errores"] = errores

    return render(request, "cargar_fichas.html", context)