# visita/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('visita/', views.visita, name='visita'),
    path('visita/registrar/', views.reservar_visita, name='registrar_visita'),
    path('visita/confirmacion/<int:visita_id>/', views.confirmacion_visita, name='confirmacion_visita'),
]