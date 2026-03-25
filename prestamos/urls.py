from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.reservar_libro, name='reservar_libro'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('aprobar/<int:prestamo_id>/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('reserva-exitosa/', views.reserva_exitosa, name='reserva_exitosa'),
    path('confirmar-prestamo/<int:prestamo_id>/', views.confirmar_prestamo, name='confirmar_prestamo'),
]