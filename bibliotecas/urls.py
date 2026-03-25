from django.urls import path
from .views import BibliotecaFormView, BibliotecaListView, index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('public/', views.public_index, name='public_index'),
    path('contacto/', views.contacto, name='contacto'),
    path('bibliotecas/', BibliotecaListView.as_view(), name='list_biblioteca'),
    path('bibliotecas/agregar/', BibliotecaFormView.as_view(), name='add_biblioteca'),
    path('detalle/<int:pk>/', views.BibliotecaDetailView.as_view(), name='detail_biblioteca'),
    path('editar/<int:pk>/', views.BibliotecaUpdateView.as_view(), name='update_biblioteca'),
    path('eliminar/<int:pk>/', views.BibliotecaDeleteView.as_view(), name='delete_biblioteca'),
    path('credencial/', views.credencial, name='credencial'),
    path('prestamos/', views.prestamo, name='prestamos'),
    path('prestamo_domicilio/', views.prestamo_domicilio, name='prestamo_domicilio'),
    path('credencializacion/', views.credencializacion, name='credencializacion'),
    path('referencia/', views.referencia, name='referencia'),
    path('servicio_digital/', views.servicio_digital, name='servicio_digital'),
    path('servicio_cultural/', views.servicio_cultural, name='servicio_cultural'),
    path('servicio_educativo/', views.servicio_educativo, name='servicio_educativo'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('coleccion_digital/', views.coleccion_digital, name='coleccion_digital'),
    path('reserva-sala/', views.reserva_sala, name='reserva_sala'),
    path('ubicaciones/', views.ubicaciones, name='ubicaciones'),
    path('visita/', views.visita, name='visita'),
    path('public_biblios/', views.public_biblios, name='public_biblios'),
]