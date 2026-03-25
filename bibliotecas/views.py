from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from bibliotecas.models import Biblioteca
from .forms import BibliotecaForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from bibliotecarios.models import Bibliotecario
from libros.models import Libro
from registros.models import Registro
from preregistro.forms import PreRegistroForm
from visita.forms import VisitaForm
from django.utils import timezone
from django.apps import apps
from eventos.models import AgendaBiblioAprende, AgendaCultural
from multiprocessing import context
from salas.models import ReservaSala
from visita.models import VisitaGuiada

User = get_user_model()

def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(es_admin)
def admin_dashboard(request):
    # Obtener la fecha y hora actual con información de zona horaria
    now = timezone.now()
    hoy = timezone.localdate()
    
    # Inicio del mes actual
    inicio_mes = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # DEBUG: Imprimir en consola
    print("="*50)
    print(f"DEBUG - Fecha actual (now): {now}")
    print(f"DEBUG - Inicio del mes: {inicio_mes}")
    print(f"DEBUG - Hoy (localdate): {hoy}")
    print(f"DEBUG - Total ReservaSala en BD: {ReservaSala.objects.count()}")
    print(f"DEBUG - Total VisitaGuiada en BD: {VisitaGuiada.objects.count()}")
    
    # Mostrar algunas fechas de la BD para comparar
    if ReservaSala.objects.exists():
        ultima_reserva = ReservaSala.objects.order_by('-created_at').first()
        print(f"DEBUG - Última reserva created_at: {ultima_reserva.created_at}")
        print(f"DEBUG - Tipo de dato: {type(ultima_reserva.created_at)}")
    
    # Contadores
    visitas_nuevas_mes_count = VisitaGuiada.objects.filter(
        created_at__gte=inicio_mes 
    ).count()
    print(f"DEBUG - Visitas nuevas mes: {visitas_nuevas_mes_count}")

    reservas_nuevas_mes_count = ReservaSala.objects.filter(
        created_at__gte=inicio_mes 
    ).count()
    print(f"DEBUG - Reservas nuevas mes: {reservas_nuevas_mes_count}")
    
    visitas_hoy_programadas_count = VisitaGuiada.objects.filter(
        fecha_visita=hoy 
    ).count()
    print(f"DEBUG - Visitas programadas hoy: {visitas_hoy_programadas_count}")
    
    # Últimas 5 visitas del mes actual
    visitas_recientes = VisitaGuiada.objects.filter(
        created_at__gte=inicio_mes
    ).order_by('-created_at')[:5]
    print(f"DEBUG - Visitas recientes encontradas: {visitas_recientes.count()}")
    
    # Últimas 5 reservas de sala del mes actual
    reservas_recientes = ReservaSala.objects.filter(
        created_at__gte=inicio_mes
    ).order_by('-created_at')[:5]
    print(f"DEBUG - Reservas recientes encontradas: {reservas_recientes.count()}")
    
    # Si no hay resultados, mostrar todas las reservas sin filtro
    if reservas_recientes.count() == 0:
        todas_reservas = ReservaSala.objects.all().order_by('-created_at')[:5]
        print(f"DEBUG - Total de reservas sin filtro: {todas_reservas.count()}")
        for r in todas_reservas:
            print(f"  - Reserva ID {r.id}: created_at = {r.created_at}")
    
    print("="*50)
    
    context = {
        'total_bibliotecas': Biblioteca.objects.count(),
        'total_bibliotecarios': User.objects.filter(groups__name='Bibliotecario').count(),
        'total_libros': Libro.objects.count(),
        'total_usuarios': User.objects.count(),
        'bibliotecas': Biblioteca.objects.all().order_by('-id')[:5],

        # Contadores
        'visitas_nuevas_mes_count': visitas_nuevas_mes_count,
        'reservas_nuevas_mes_count': reservas_nuevas_mes_count,
        'visitas_hoy_programadas_count': visitas_hoy_programadas_count,
        'visitas_nuevas_hoy_count': visitas_nuevas_mes_count,
        'reservas_nuevas_hoy_count': reservas_nuevas_mes_count,
        
        # Registros recientes
        'visitas_recientes': visitas_recientes,
        'reservas_recientes': reservas_recientes,
    }
    
    context['total_bibliotecarios'] = Bibliotecario.objects.count()
    context['bibliotecarios'] = Bibliotecario.objects.all().order_by('-fecha_creacion')[:5]
    context['libros'] = Libro.objects.all().order_by('-fecha_creacion')[:5]
    
    return render(request, 'admin_dashboard.html', context)


class BibliotecaFormView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    template_name = 'bibliotecas/add_biblioteca.html'
    form_class = BibliotecaForm
    success_url = reverse_lazy("add_biblioteca")
    login_url = '/login/' 
    
    def test_func(self):
        # Comprueba si el usuario tiene permisos administrativos
        return es_admin(self.request.user)
        
    def handle_no_permission(self):
        # Redirige si no tiene permisos
        if self.request.user.is_authenticated:

            return redirect('acceso_denegado')  # Crea esta vista

        return redirect(f"{self.login_url}?next={self.request.path}")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class BibliotecaListView(LoginRequiredMixin, generic.ListView):
    model = Biblioteca
    template_name = 'bibliotecas/list_biblioteca.html'
    context_object_name = 'bibliotecas'
    paginate_by = 10 
    
    def get_queryset(self):
        queryset = Biblioteca.objects.all()
        search = self.request.GET.get('search')
        
        if search:

            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(nombre_corto__icontains=search) | 
                Q(direccion__icontains=search) | 
                Q(ubicacion__icontains=search) |
                Q(director__icontains=search) |
                Q(telefono__icontains=search) |
                Q(email__icontains=search) |
                Q(reseña__icontains=search)
            )
        
        return queryset


class BibliotecaDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Biblioteca
    template_name = 'bibliotecas/biblioteca_detail.html'
    context_object_name = 'biblioteca'
    
    def test_func(self):
        return es_admin(self.request.user)

# NUEVA VISTA - Actualizar Biblioteca (UPDATE)
# Vista para actualizar Biblioteca con manejo correcto de formularios
class BibliotecaUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Biblioteca
    form_class = BibliotecaForm
    template_name = 'bibliotecas/biblioteca_form.html'
    success_url = reverse_lazy('list_biblioteca')
    
    def test_func(self):
        return es_admin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['biblioteca_id'] = self.object.id
        return context
    
    def get_initial(self):
        # Garantizar que los valores iniciales se cargan correctamente
        initial = super().get_initial()
        for field in self.form_class.Meta.fields:
            if hasattr(self.object, field):
                initial[field] = getattr(self.object, field)
        return initial
    
    def form_valid(self, form):
        print(f"Form is valid! Changed data: {form.changed_data}")
        
        # Si hay una foto nueva, la imagen anterior debe ser eliminada
        if 'foto' in form.changed_data and self.object.foto:
            self.object.foto.delete(save=False)

        self.object = form.save()

        messages.success(self.request, f"La biblioteca '{self.object.nombre}' ha sido actualizada correctamente.")
        
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        print(f"Form is invalid! Errors: {form.errors}")
        return super().form_invalid(form)


class BibliotecaDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Biblioteca
    template_name = 'bibliotecas/biblioteca_confirm_delete.html'
    success_url = reverse_lazy('list_biblioteca')
    context_object_name = 'biblioteca'
    
    def test_func(self):
        return es_admin(self.request.user)
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect(success_url)


def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

def index(request):

    total_usuarios = Registro.objects.count()
    
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Vista de administrador
            context = {
                'total_usuarios': total_usuarios,

            }
            return render(request, 'admin_dashboard.html', context)
        else:
            # Vista de usuario registrado
            context = {
                'total_usuarios': total_usuarios,
            }
            return render(request, 'users/user_dashboard.html', context)
    else:
        # Visitante no autenticado
        context = {
            'total_usuarios': total_usuarios,
        }
        return render(request, 'public/public_index.html', context)


def public_index(request):

    ultimos_libros = Libro.objects.order_by('fecha_creacion')[:4]
    return render(request, 'public/public_index.html', {'ultimos_libros': ultimos_libros})


def contacto(request):
    return render(request, 'public/contact.html')

def prestamo(request):
    return render(request, 'public/prestamo.html')

def prestamo_domicilio(request):
    return render(request, 'public/prestamo_domicilio.html')

def credencializacion(request):
    return render(request, 'public/credencializacion.html')

def referencia(request):
    return render(request, 'public/referencia.html')

def servicio_digital(request):
    return render(request, 'public/servicio_digital.html')

def servicio_cultural(request):
    return render(request, 'public/servicio_cultural.html')

def servicio_educativo(request):
    return render(request, 'public/servicio_educativo.html')

def nosotros(request):
    return render(request, 'public/nosotros.html')

def credencial(request):
    form = PreRegistroForm()  # Crear una instancia del formulario
    return render(request, 'public/credencial.html', {'form': form})

def coleccion_digital(request):
    return render(request, 'public/coleccion_digital.html')

def reserva_sala(request):
    return render(request, 'public/salas.html')

def ubicaciones(request):
    return render(request, 'public/ubicaciones.html')

def visita(request):
    form = VisitaForm()
    return render(request, 'public/visita.html', {'form': form})


def public_biblios(request):
    # 1. Obtener la consulta de búsqueda
    search_query = request.GET.get('search')
    
    # 2. Iniciar el QuerySet base con todas las bibliotecas
    bibliotecas = Biblioteca.objects.all() 
    
    # 3. ¡ESTA ES LA LÓGICA QUE FALTABA! Aplicar el filtro si hay una consulta
    if search_query:
        # Filtra por el campo 'nombre' que contenga el término de búsqueda,
        # ignorando mayúsculas y minúsculas (icontains).
        
        # Opciones de Filtrado:
        
        # Opción A: Búsqueda simple por nombre (más común en vistas públicas)
        bibliotecas = bibliotecas.filter(nombre__icontains=search_query) 
        
        # Opción B: Búsqueda multi-campo (como en tu ListView original, si la prefieres)
        # bibliotecas = bibliotecas.filter(
        #     Q(nombre__icontains=search_query) | 
        #     Q(nombre_corto__icontains=search_query) | 
        #     Q(direccion__icontains=search_query)
        #     # ... añade más campos si es necesario
        # )

    # 4. Renderizar el template con el QuerySet filtrado (o completo si no había búsqueda)
    context = {
        'bibliotecas': bibliotecas,
        'search_query': search_query # Se usa para mantener el texto en el input
    }
    
    return render(request, 'public/public_biblios.html', context)
