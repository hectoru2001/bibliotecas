# projects/bibliotecarios/views.py
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .models import Bibliotecario
from .forms import BibliotecarioForm
from django.shortcuts import redirect
from django.urls import reverse

class PermRedirectMixin:
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('admin_dashboard')
        login_url = reverse('login')
        return redirect(f'{login_url}?next={self.request.path}')

class BibliotecaScopeMixin:
    """Limita querysets a la biblioteca del bibliotecario logueado (salvo superuser)."""
    def get_user_biblioteca_id(self):
        bprof = getattr(self.request.user, 'bibliotecario', None)
        return getattr(bprof, 'biblioteca_id', None)

    def scope_queryset(self, qs):
        if self.request.user.is_superuser:
            return qs
        bid = self.get_user_biblioteca_id()
        return qs.filter(biblioteca_id=bid) if bid else qs.none()


class BibliotecarioListView(LoginRequiredMixin, PermissionRequiredMixin, PermRedirectMixin ,BibliotecaScopeMixin, generic.ListView):
    permission_required = 'bibliotecarios.view_bibliotecario'
    raise_exception = True

    model = Bibliotecario
    template_name = 'bibliotecarios/list_bibliotecario.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        qs = self.scope_queryset(super().get_queryset())
        search = self.request.GET.get('search') or ''
        if search:
            qs = qs.filter(
                Q(nombre__icontains=search) |
                Q(apellido__icontains=search) |
                Q(email__icontains=search) |
                Q(biblioteca__nombre__icontains=search)
            )
        return qs.order_by('apellido', 'nombre')

class BibliotecarioFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """CreateView con el nombre que ya usas en urls (`add_bibliotecario`)."""
    permission_required = 'bibliotecarios.add_bibliotecario'
    raise_exception = True

    model = Bibliotecario
    form_class = BibliotecarioForm
    template_name = 'bibliotecarios/add_bibliotecario.html'
    success_url = reverse_lazy('list_bibliotecario')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user   # ← para que el form limite Bibliotecas
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        # registra quién lo creó si tu modelo lo tiene
        if hasattr(obj, 'created_by') and not obj.created_by_id:
            obj.created_by = self.request.user
        obj.save()
        return super().form_valid(form)

class BibliotecarioDetailView(LoginRequiredMixin, PermissionRequiredMixin, BibliotecaScopeMixin, generic.DetailView):
    permission_required = 'bibliotecarios.view_bibliotecario'
    raise_exception = True

    model = Bibliotecario
    template_name = 'bibliotecarios/detail_bibliotecario.html'
    context_object_name = 'obj'

    def get_queryset(self):
        return self.scope_queryset(super().get_queryset())

class BibliotecarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, BibliotecaScopeMixin, generic.UpdateView):
    permission_required = 'bibliotecarios.change_bibliotecario'
    raise_exception = True

    model = Bibliotecario
    form_class = BibliotecarioForm
    template_name = 'bibliotecarios/edit_bibliotecario.html'
    success_url = reverse_lazy('list_bibliotecario')

    def get_queryset(self):
        return self.scope_queryset(super().get_queryset())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

class BibliotecarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, BibliotecaScopeMixin, generic.DeleteView):
    permission_required = 'bibliotecarios.delete_bibliotecario'
    raise_exception = True

    model = Bibliotecario
    template_name = 'bibliotecarios/confirm_delete.html'
    success_url = reverse_lazy('list_bibliotecario')

    def get_queryset(self):
        return self.scope_queryset(super().get_queryset())
