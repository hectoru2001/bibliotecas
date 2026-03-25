from django.urls import path
from .views import importar_fichas

urlpatterns = [
    path('cargar_fichas/', importar_fichas, name="carga_fichas"),
]