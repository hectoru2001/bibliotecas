import csv
import subprocess
import os
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from fichas.models import Ficha, ImportacionFicha


def to_int(valor):
    try:
        return int(valor)
    except:
        return None


def safe_parse_datetime(valor):
    if valor in (None, '', 'NULL'):
        return None

    if isinstance(valor, datetime):
        dt = valor
    else:
        valor = str(valor).strip()

        dt = parse_datetime(valor)
        if not dt:
            formatos = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%m/%d/%y %H:%M:%S",
                "%m/%d/%y",
            ]

            for f in formatos:
                try:
                    dt = datetime.strptime(valor, f)
                    break
                except:
                    continue

    if not dt:
        return None

    if timezone.is_naive(dt):
        tz = pytz.timezone('America/Chihuahua')
        dt = tz.localize(dt)

    return dt


class Command(BaseCommand):
    help = "Procesa fichas en background"

    def add_arguments(self, parser):
        parser.add_argument('imp_id', type=int)


    def handle(self, *args, **kwargs):
        imp_id = kwargs['imp_id']
        
        imp = ImportacionFicha.objects.get(id=imp_id)

        imp.estado = "procesando"
        imp.save()

        ruta = imp.archivo.path

        try:
            tabla = subprocess.check_output(
                ["mdb-tables", "-1", ruta]
            ).decode().splitlines()[0]

            proceso = subprocess.Popen(
                ["mdb-export", ruta, tabla],
                stdout=subprocess.PIPE,
                text=True
            )

            lector = csv.DictReader(proceso.stdout)

            batch = []
            total = 0

            for fila in lector:

                ficha_no = to_int(fila.get("Ficha_No"))
                if not ficha_no:
                    continue

                obj = Ficha(
                    ficha_no=ficha_no,
                    fecha=safe_parse_datetime(fila.get("Fecha")),
                    fechamod=safe_parse_datetime(fila.get("FechaMod")),
                    datosfijos=fila.get("DatosFijos"),
                    etiquetasmar=fila.get("EtiquetasMARC"),
                    tipomaterial=to_int(fila.get("TipoMaterial")) or 0,
                    isbn=fila.get("ISBN"),
                    titulo=fila.get("Titulo"),
                    autor=fila.get("Autor"),
                    clasificacion=fila.get("Clasificacion"),
                )

                batch.append(obj)

                if len(batch) >= 1000:
                    Ficha.objects.bulk_create(batch, ignore_conflicts=True)
                    batch = []

                total += 1

            if batch:
                Ficha.objects.bulk_create(batch, ignore_conflicts=True)

            imp.estado = "terminado"
            imp.total = total
            imp.save()

        except Exception as e:
            imp.estado = "error"
            imp.error = str(e)
            imp.save()