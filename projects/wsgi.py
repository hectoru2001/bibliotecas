"""
WSGI config for projects project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
# -*- coding: utf-8 -*-

import os
# --- INICIO DE SOLUCIÓN DE CODIFICACIÓN ---
import locale
# FUERZA LA CONFIGURACIÓN REGIONAL A UTF-8 antes de cargar Django
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
# --- FIN DE SOLUCIÓN DE CODIFICACIÓN ---

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')

application = get_wsgi_application()