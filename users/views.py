# from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # Importar el formulario personalizado
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView  # AÃ‘ADIR ESTA IMPORTACIÃ“N
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from registros.models import Registro  # Asumiendo que este es tu modelo de usuario
from .forms import UserAdminForm
from prestamos.models import Prestamo
from django.db.models import Q


User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        u = self.request.user
        next_url = self.request.GET.get('next')

        # Admines: respetamos ?next=... (si llegÃ³ desde una vista protegida de admin)
        if next_url and (u.is_superuser or u.groups.filter(name__in=['AdminSistema','AdminBiblioteca']).exists()):
            return next_url

        # Admines: panel completo
        if u.is_superuser or u.groups.filter(name__in=['AdminSistema','AdminBiblioteca']).exists():
            return reverse_lazy('admin_dashboard')

        # Bibliotecario: a Libros (o cambia a 'user_list' si prefieres)
        if u.groups.filter(name='Bibliotecario').exists() or getattr(u, 'role', '') == 'librarian':
            return reverse_lazy('list_libro')

        # Otros roles: decide un destino por defecto
        return reverse_lazy('user_dashboard')

    

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm  # Usar el formulario personalizado
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

@login_required
def perfil_usuario(request):
    # Si tienes un modelo de PrÃ©stamos, puedes incluirlo aquÃ­
    prestamos = Prestamo.objects.filter(usuario=request.user).order_by('-fecha_prestamo')[:5]
    
    # Si no tienes el modelo aÃºn, usa una lista vacÃ­a
    prestamos = []
    
    return render(request, 'users/perfil.html', {
        'user': request.user,
        'prestamos': prestamos,
    })

# Agregar al final del archivo views.py de users
@login_required
def user_dashboard(request):
    """Vista para el dashboard de usuarios normales"""
    return render(request, 'users/user_dashboard.html')

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario sea administrador"""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Registro
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    permission_required = 'registros.view_registro'

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = (Registro.objects
              .select_related('fiador', 'biblioteca')
              .order_by('-created_at'))
        # (Opcional) limita por biblioteca al bibliotecario
        u = self.request.user
        bprof = getattr(u, 'bibliotecario', None)
        if bprof and not u.is_superuser:
            qs = qs.filter(biblioteca=bprof.biblioteca)

        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(nombres__icontains=q) |
                Q(apellido_paterno__icontains=q)
            )
        return qs


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Registro
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'  # Cambiamos a user_obj para evitar conflicto con request.user

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Registro
    form_class = UserAdminForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('admin_user_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear nuevo usuario'
        context['button_text'] = 'Crear usuario'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Usuario creado exitosamente.")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Registro
    form_class = UserAdminForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('admin_user_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['button_text'] = 'Guardar cambios'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado exitosamente.")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Registro
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('admin_user_list')
    context_object_name = 'user_obj'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)