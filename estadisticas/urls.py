from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stats_y_datos, name='stats_form'),
    path('stats/submit/', views.stats_y_datos, name='submit_stats'),
    path('stats/confirmation/', views.confirmation, name='confirmation'),
    path('stats/monthly-log/', views.monthly_log, name='monthly_log'),
]

