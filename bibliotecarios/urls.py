# projects/bibliotecarios/urls.py
from django.urls import path
from .views import (
    BibliotecarioListView,
    BibliotecarioFormView,
    BibliotecarioDetailView,
    BibliotecarioUpdateView,
    BibliotecarioDeleteView,
)

urlpatterns = [
    path('', BibliotecarioListView.as_view(), name='list_bibliotecario'),
    path('agregar/', BibliotecarioFormView.as_view(), name='add_bibliotecario'),
    path('detalle/<int:pk>/', BibliotecarioDetailView.as_view(), name='detail_bibliotecario'),
    path('<int:pk>/editar/', BibliotecarioUpdateView.as_view(), name='update_bibliotecario'),
    path('<int:pk>/eliminar/', BibliotecarioDeleteView.as_view(), name='delete_bibliotecario'),
]
