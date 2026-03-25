from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReservaForm
from .models import Prestamo
from django.utils import timezone
from datetime import timedelta

@login_required
def reservar_libro(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.save()
                return redirect('reserva_exitosa')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = ReservaForm(initial={'libro_id': request.GET.get('libro_id')}, user=request.user)
    return render(request, 'prestamos/reservar_libro.html', {'form': form})

@staff_member_required
def dashboard_admin(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamos/dashboard_admin.html', {'prestamos': prestamos})

@staff_member_required
def aprobar_prestamo(request, prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)
    if request.method == 'POST':
        form = AprobarPrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo.estado = 'prestado'
            form.save()
            prestamo.save()
            return redirect('dashboard_admin')
    else:
        form = AprobarPrestamoForm(instance=prestamo)
    return render(request, 'prestamos/aprobar_prestamo.html', {'form': form, 'prestamo': prestamo})

def reserva_exitosa(request):
    return render(request, 'prestamos/reserva_exitosa.html')

@staff_member_required
def confirmar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, estado='reservado')
    if request.method == 'POST':
        # Actualizar el estado del préstamo
        prestamo.estado = 'prestado'
        prestamo.fecha_prestamo = timezone.now()
        prestamo.fecha_devolucion = timezone.now() + timedelta(days=7)
        prestamo.save()
        return render(request, 'prestamos/prestamo_success.html', {'prestamo': prestamo})
    return render(request, 'prestamos/confirmar_prestamo.html', {'prestamo': prestamo})