# preregistro/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('pre-registro/', views.pre_registro, name='pre_registro'),
    path('confirmacion-pre-registro/<int:pre_registro_id>/', views.confirmacion_pre_registro, name='confirmacion_pre_registro'),
]
