from django.urls import path
from .views import FiadorFormView, FiadorListView

urlpatterns = [
    path('registrar/', FiadorFormView, name='add_fiador'),
    path('success/', FiadorListView, name='exitoso_fiador'),
]
