from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stats_form, name='stats_form'),
    path('stats/submit/', views.stats_form, name='submit_stats'),
    path('stats/confirmation/', views.confirmation, name='confirmation'),
    path('stats/datos-estadisticos/', views.datos_estadisticos, name='datos_estadisticos'),
    path('stats/monthly-log/', views.monthly_log, name='monthly_log'),
]

