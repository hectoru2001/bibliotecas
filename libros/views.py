from django.shortcuts import redirect, render, get_object_or_404 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Libro
from .forms import LibroForm
from bibliotecas.models import Biblioteca  # Para poder seleccionar bibliotecas
from libros.models import Libro
from fichas.models import Ficha


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class LibroListView(LoginRequiredMixin, StaffRequiredMixin, generic.ListView):
    model = Libro
    template_name = 'libros/list_libro.html'
    context_object_name = 'object_list'
    paginate_by = 50  # Aumentamos a 50 para mejor rendimiento

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                models.Q(titulo__icontains=search) | 
                models.Q(autor__icontains=search) | 
                models.Q(isbn__icontains=search) |
                models.Q(editorial__icontains=search) |
                models.Q(biblioteca__nombre__icontains=search)
            )

        # Filtrar por estado
        estado = self.request.GET.get('estado', '')
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

class LibroCreateView(LoginRequiredMixin, StaffRequiredMixin, generic.CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/add_libro.html'
    success_url = reverse_lazy('list_libro')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.role = 'admin'  # Asignar el rol adecuado
        messages.success(self.request, f"El libro '{form.instance.titulo}' ha sido creado exitosamente.")
        return super().form_valid(form)

class LibroFormView(LoginRequiredMixin, StaffRequiredMixin, generic.FormView):
    template_name = 'libros/add_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('list_libro')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bibliotecas'] = Biblioteca.objects.all()
        return context
    def form_valid(self, form):
        libro = form.save(commit=False)
        libro.created_by = self.request.user
        
       
        numadqui = self.request.POST.get('numadqui')
        if numadqui:
            try:
                ficha = Ficha.objects.get(ficha_no=numadqui)
                libro.numadqui = ficha
            except Ficha.DoesNotExist:
                form.add_error(None, "La ficha seleccionada no existe.")
                return self.form_invalid(form)
        
        libro.save()
        messages.success(self.request, f"El libro '{libro.titulo}' ha sido agregado correctamente.")
        return super().form_valid(form)


class LibroDetailView(LoginRequiredMixin, StaffRequiredMixin, generic.DetailView):
    model = Libro
    template_name = 'libros/libro_detail.html'
    context_object_name = 'libro'

class LibroUpdateView(LoginRequiredMixin, StaffRequiredMixin, generic.UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    context_object_name = 'libro'
    success_url = reverse_lazy('list_libro')
    
    def form_valid(self, form):
        messages.success(self.request, f"El libro '{form.instance.titulo}' ha sido actualizado exitosamente.")
        return super().form_valid(form)

class LibroDeleteView(LoginRequiredMixin, StaffRequiredMixin, generic.DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html'
    context_object_name = 'libro'
    success_url = reverse_lazy('list_libro')
    
    def delete(self, request, *args, **kwargs):
        libro = self.get_object()
        messages.success(request, f"El libro '{libro.titulo}' ha sido eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

def search_ficha(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        if query:
            fichas = Ficha.objects.filter(
                Q(ficha_no__icontains=query) |
                Q(titulo__icontains=query) |
                Q(autor__icontains=query)
            ).values('ficha_no', 'titulo', 'autor', 'isbn')[:10]  # Limitamos a 10 resultados
            return JsonResponse({'fichas': list(fichas)}, status=200)
        return JsonResponse({'fichas': []}, status=200)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)


# def public_books(request):
#     libros = Libro.objects.all()  # Obtiene todos los libros
#     return render(request, 'public/public_books.html', {'libros': libros})

def public_books(request):
    libros = Libro.objects.all()


    query = request.GET.get('q', '')
    if query:
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query) | libros.filter(isbn__icontains=query)

    # Filtro por estado
    status = request.GET.get('status', '')
    if status == 'available':
        libros = libros.filter(estado=Libro.Estado.AVAILABLE)
    elif status == 'reserved':
        libros = libros.filter(estado=Libro.Estado.RESERVED)
    elif status == 'not_available':
        libros = libros.filter(estado__in=[Libro.Estado.LOANED, Libro.Estado.MAINTENANCE, Libro.Estado.LOST])

    return render(request, 'public/public_books.html', {'libros': libros})