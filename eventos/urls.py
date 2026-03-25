# eventos/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('eventos/gestor/', views.event_list, name='event_list'),

    # BiblioAprende (público + CRUD)
    path('biblioaprende/', views.lista_biblioaprende, name='lista_biblioaprende'),
    path('biblioaprende/crear/', views.crear_biblioaprende, name='crear_biblioaprende'),
    path('eventos/biblioaprende/<int:pk>/editar/', views.editar_biblioaprende, name='editar_biblioaprende'),
    path('eventos/biblioaprende/<int:pk>/eliminar/', views.eliminar_biblioaprende, name='eliminar_biblioaprende'),

    # Agenda cultural (público + CRUD)
    path('agenda-cultural/', views.agenda_cultural, name='agenda_cultural'),
    path('crear-agenda-cultural/', views.crear_agenda_cultural, name='crear_agenda_cultural'),
    path('eventos/agenda-cultural/<int:pk>/editar/', views.editar_agenda_cultural, name='editar_agenda_cultural'),
    path('eventos/agenda-cultural/<int:pk>/eliminar/', views.eliminar_agenda_cultural, name='eliminar_agenda_cultural'),
]
