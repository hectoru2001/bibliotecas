# bibliotecarios/apps.py
from django.apps import AppConfig

class BibliotecariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bibliotecarios'

    def ready(self):
        from . import signals  # noqa: F401
