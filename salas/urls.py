
from django.urls import path
from . import views

urlpatterns = [
    path('salas/', views.salas, name='salas'),
    path('salas/registrar/', views.reservar_sala, name='reservar_sala'),
    path('salas/confirmar/', views.confirmar_sala, name='confirmar_sala'),

]