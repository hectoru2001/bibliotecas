import csv
import subprocess
import tempfile
import os
import pytz
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.db import transaction
from .models import Ficha
import subprocess
from django.shortcuts import render
from .models import ImportacionFicha


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

def importar_fichas(request):

    if request.method == "POST" and request.FILES.get("archivo"):

        archivo = request.FILES["archivo"]

        imp = ImportacionFicha.objects.create(
            archivo=archivo,
            estado="pendiente"
        )

        log_file = open("/tmp/procesar.log", "a")

        subprocess.Popen(
            [
                "/home/asalas/Produccion/Bibliotecas/venv/bin/python",
                "/home/asalas/Produccion/Bibliotecas/manage.py",
                "procesar_fichas",
                str(imp.id)
            ],
            stdout=log_file,
            stderr=log_file,
            env={"PYTHONUNBUFFERED": "1"}
        )

        return render(request, "cargar_fichas.html", {
            "mensaje": f"Archivo subido. Importación #{imp.id} en proceso."
        })

    # 👇 GET o sin archivo
    return render(request, "cargar_fichas.html")