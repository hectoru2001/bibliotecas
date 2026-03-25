
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
def health_check(request):
    return HttpResponse("OK", status=200)

from bibliotecas.views import admin_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', include('bibliotecas.urls')),
    path('bibliotecas/', include('bibliotecas.urls')),
    path('usuarios/', include('users.urls')),  
    path('bibliotecarios/', include('bibliotecarios.urls')),
    path('libros/', include('libros.urls')),
    path('registros/', include('registros.urls')),
    path('fiadores/', include('fiadores.urls')),
    path('', include('preregistro.urls')),
    path('', include('visita.urls')),
    path('', include('salas.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('prestamos/', include('prestamos.urls')),
    path('estadisticas/', include('estadisticas.urls')),
    path('eventos/', include('eventos.urls')),
    path('fichas/', include('fichas.urls')),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Al final del archivo, después de las urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


