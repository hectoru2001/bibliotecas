from django.urls import path
from .views import LibroListView, LibroCreateView
from . import views

urlpatterns = [
    path('', views.LibroListView.as_view(), name='list_libro'),
    # path('agregar/', views.LibroFormView.as_view(), name='add_libro'),
    path('agregar/', LibroCreateView.as_view(), name='add_libro'),
    path('<int:pk>/', views.LibroDetailView.as_view(), name='detail_libro'),
    path('<int:pk>/editar/', views.LibroUpdateView.as_view(), name='update_libro'),
    path('<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='delete_libro'),
    path('search_ficha/', views.search_ficha, name='search_ficha'),
    path('public_books/', views.public_books, name='public_books'),
]