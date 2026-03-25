from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import transaction, IntegrityError
from preregistro.models import PreRegistro
from .forms import RegistroForm  # Importación relativa correcta
from .models import Registro
from .forms import RegistroFiadorForm  # Asegúrate de importar el nuevo formulario
from fiadores.models import Fiador
from fiadores.forms import FiadorForm
from datetime import date, timedelta
from django.contrib.auth import get_user_model
import logging
from bibliotecas.models import Biblioteca
from django.http import JsonResponse
from django.db.models import Q


# Configurar logger para depuración
logger = logging.getLogger(__name__)
User = get_user_model()


class BuscarPreRegistros(View):
    def get(self, request):
        query = request.GET.get('q', '')
        pre_registros = PreRegistro.objects.filter(
            is_active=False
        ).filter(
            Q(nombres__icontains=query) | Q(email__icontains=query) | Q(apellido_paterno__icontains=query) | Q(apellido_materno__icontains=query)
        )
        data = [{
            'id': pr.id,
            'nombre': f"{pr.nombres} {pr.apellido_paterno} {pr.apellido_materno}",
            'email': pr.email,
            'nombres': pr.nombres, 
            'apellido_paterno': pr.apellido_paterno,
            'apellido_materno': pr.apellido_materno,
        } for pr in pre_registros]
        return JsonResponse({'pre_registros': data})

class RegistroPaso1(View):

    def get(self, request):
        form = RegistroForm()
        # Obtener pre-registros pendientes (por ejemplo, donde is_active=False)
        pre_registros = PreRegistro.objects.filter(is_active=False)
        return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})

        
    def post(self, request):
        form = RegistroForm(request.POST)
        # Obtener pre-registros pendientes para re-renderizar la tabla si falla el POST
        pre_registros = PreRegistro.objects.filter(is_active=False) 
        
        # Log para depuración
        logger.info(f"Datos del formulario recibidos: {request.POST}")
        
        if form.is_valid():
            # Verificar que el email no esté ya en uso
            email = form.cleaned_data['email']
            if email and User.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo electrónico ya está en uso')
                messages.error(request, "Este correo electrónico ya está en uso")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})
          
            # Verificar que el username no esté ya en uso
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Este nombre de usuario ya está en uso')
                messages.error(request, "Este nombre de usuario ya está en uso")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})
            
            # Verificar que las contraseñas coincidan
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data.get('confirm_password')
            if password != confirm_password:
                form.add_error('confirm_password', 'Las contraseñas no coinciden')
                messages.error(request, "Las contraseñas no coinciden")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})
                
            # Guardamos los datos del formulario en la sesión
            try:
                biblioteca = form.cleaned_data.get('biblioteca')
                biblioteca_id = None
                
                if biblioteca:
                    biblioteca_id = biblioteca.id
                else:
                    # Intentar obtener la primera biblioteca disponible
                    primera_biblioteca = Biblioteca.objects.first()
                    if primera_biblioteca:
                        biblioteca_id = primera_biblioteca.id
                    else:
                        # Si no hay bibliotecas, mostrar error
                        messages.error(request, "No hay bibliotecas disponibles para el registro. Contacte al administrador.")
                        return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})
                
                # Guardar todos los datos necesarios en la sesión para el siguiente paso
                request.session['registro_data'] = {
                    'nombres': form.cleaned_data['nombres'],
                    'apellido_paterno': form.cleaned_data['apellido_paterno'],
                    'apellido_materno': form.cleaned_data['apellido_materno'],
                    'edad': form.cleaned_data['edad'],
                    'domicilio': form.cleaned_data['domicilio'],
                    'codigo_postal': form.cleaned_data['codigo_postal'],
                    'telefono': form.cleaned_data['telefono'],
                    'email': email,
                    'username': username,
                    'password': password,
                    'ocupacion': form.cleaned_data['ocupacion'],
                    'escuela_trabajo': form.cleaned_data['escuela_trabajo'],
                    'telefono_escuela_trabajo': form.cleaned_data['telefono_escuela_trabajo'],
                    'role': form.cleaned_data['role'],
                    'biblioteca_id': biblioteca_id,
                    'curp': form.cleaned_data['curp'],
                    
                }
                request.session.modified = True
                
                logger.info(f"Datos de registro guardados en sesión: {request.session['registro_data'].keys()}")
                return redirect('registro_paso2')
            except Exception as e:
                logger.error(f"Error al guardar datos en sesión: {str(e)}")
                messages.error(request, f"Error al procesar el formulario: {str(e)}")
        else:
            logger.error(f"Formulario inválido: {form.errors}")
            
            # Mostrar errores detallados para cada campo
            for field_name, error_list in form.errors.items():
                for error in error_list:
                    # Obtener nombre legible del campo
                    if field_name == 'biblioteca' and error == 'Este campo es obligatorio.':
                        messages.error(request, "Debes seleccionar una biblioteca. Si no hay opciones, contacta al administrador.")
                    else:
                        field_label = form[field_name].label if hasattr(form[field_name], 'label') else field_name
                        messages.error(request, f"Error en {field_label}: {error}")
            
            # Mensaje general al final
            messages.error(request, "Por favor corrige los errores señalados en el formulario.")
            
        return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros})


# CLASE PARA EL PRELLENADO (Actualizada para mejor depuración de errores)
class RegistroPaso1Prellenar(View):
    
    # 1. Método GET: Carga los datos del pre-registro
    def get(self, request, pre_registro_id):
        # 1.1 Obtener el pre-registro usando el ID de la URL
        pre_registro = get_object_or_404(PreRegistro, pk=pre_registro_id)
        
        # 1.2 Mapear los datos del pre-registro para usar en 'initial' del formulario
        initial_data = {
            'nombres': pre_registro.nombres,
            'apellido_paterno': pre_registro.apellido_paterno,
            'apellido_materno': pre_registro.apellido_materno,
            'telefono': pre_registro.telefono,
            'email': pre_registro.email,
            'username': pre_registro.username,
            'ocupacion': pre_registro.ocupacion,
            'escuela_trabajo': pre_registro.escuela_trabajo,
            'domicilio': pre_registro.domicilio,
            'codigo_postal': pre_registro.codigo_postal,
        }
        
        # 1.3 Crear el formulario, inicializándolo con los datos del pre-registro
        form = RegistroForm(initial=initial_data)

        # 1.4 Obtener lista de pre-registros para la tabla
        pre_registros = PreRegistro.objects.filter(is_active=False)
        
        # 1.5 Crear el objeto de datos para rellenar el template (esencial para los campos 'value=')
        pre_registro_data = {
            'id': pre_registro.id,
            **initial_data 
        }
        
        context = {
            'form': form,
            'pre_registros': pre_registros,
            'pre_registro_data': pre_registro_data, # Usado por el template para prellenar campos
        }
        
        messages.info(request, f"Datos del Pre-Registro ID: {pre_registro_id} cargados. Por favor, complete la contraseña y continúe.")
        return render(request, 'registros/registro_paso1.html', context)
    
    # 2. Método POST: Procesa el formulario prellenado
    def post(self, request, pre_registro_id):
        # 2.1 Obtener pre-registros pendientes para re-renderizar la tabla si falla el POST
        pre_registros = PreRegistro.objects.filter(is_active=False)
        form = RegistroForm(request.POST)

        if form.is_valid():
            
            # --- VALIDACIONES ADICIONALES ---
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data.get('confirm_password')

            # Aseguramos que el email y username no estén en uso por OTROS usuarios
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo electrónico ya está en uso por otro usuario.')
                messages.error(request, "Este correo electrónico ya está en uso por otro usuario.")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros, 'pre_registro_data': request.POST})

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Este nombre de usuario ya está en uso por otro usuario.')
                messages.error(request, "Este nombre de usuario ya está en uso por otro usuario.")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros, 'pre_registro_data': request.POST})
            
            if password != confirm_password:
                form.add_error('confirm_password', 'Las contraseñas no coinciden')
                messages.error(request, "Las contraseñas no coinciden")
                return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros, 'pre_registro_data': request.POST})
            # --- FIN VALIDACIONES ADICIONALES ---

            
            # --- ZONA CRÍTICA: GESTIÓN DE DATOS ---
            try:
                # 2.2 Iniciar una transacción para garantizar la atomicidad
                with transaction.atomic():
                    
                    # 2.3 Obtener la biblioteca
                    biblioteca = form.cleaned_data.get('biblioteca')
                    biblioteca_id = None
                    if biblioteca:
                        biblioteca_id = biblioteca.id
                    else:
                        primera_biblioteca = Biblioteca.objects.first()
                        if primera_biblioteca:
                            biblioteca_id = primera_biblioteca.id
                        else:
                            messages.error(request, "No hay bibliotecas disponibles. Contacte al administrador.")
                            return render(request, 'registros/registro_paso1.html', {'form': form, 'pre_registros': pre_registros, 'pre_registro_data': request.POST})

                    # 2.4 Guardar los datos del formulario en la sesión
                    request.session['registro_data'] = {
                        'nombres': form.cleaned_data['nombres'],
                        'apellido_paterno': form.cleaned_data['apellido_paterno'],
                        'apellido_materno': form.cleaned_data['apellido_materno'],
                        'edad': form.cleaned_data['edad'],
                        'domicilio': form.cleaned_data['domicilio'],
                        'codigo_postal': form.cleaned_data['codigo_postal'],
                        'curp': form.cleaned_data['curp'],
                        'telefono': form.cleaned_data['telefono'],
                        'email': email,
                        'username': username,
                        'password': password,
                        'ocupacion': form.cleaned_data['ocupacion'],
                        'escuela_trabajo': form.cleaned_data['escuela_trabajo'],
                        'telefono_escuela_trabajo': form.cleaned_data['telefono_escuela_trabajo'],
                        'role': form.cleaned_data['role'],
                        'biblioteca_id': biblioteca_id,

                    }
                    request.session.modified = True
                    
                    # 2.5 LOCALIZAR Y ELIMINAR EL PRE-REGISTRO
                    pre_registro = PreRegistro.objects.get(pk=pre_registro_id)
                    pre_registro.delete() 
                    messages.success(request, f"Pre-registro ID: {pre_registro_id} procesado y eliminado. Continúe con el paso 2.")
                    
                    # 2.6 CONTINUAR AL SIGUIENTE PASO
                    return redirect('registro_paso2') 

            except PreRegistro.DoesNotExist:
                messages.error(request, 'Error grave: El pre-registro original fue eliminado justo antes de procesarlo.')
                return redirect('registro_paso1')

            except Exception as e:
                # Capturamos otros errores (ej. de DB)
                logger.error(f"Error al procesar el pre-registro (DB/Session): {e}")
                messages.error(request, f'Ocurrió un error al guardar el registro: {e}')
        

        logger.error(f"Formulario inválido en prellenado (Paso 1): {form.errors}")
        
        # Mantenemos los datos POST para que los campos del template se rellenen automáticamente
        pre_registro_data = request.POST 

        # Replicamos la lógica de mensajes de error para que el usuario sepa qué corregir
        for field_name, error_list in form.errors.items():
            for error in error_list:
                if field_name == 'biblioteca' and error == 'Este campo es obligatorio.':
                    messages.error(request, "Debes seleccionar una biblioteca. Si no hay opciones, contacta al administrador.")
                else:
                    field_label = form[field_name].label if hasattr(form[field_name], 'label') else field_name
                    messages.error(request, f"Error en {field_label}: {error}")
        
        messages.error(request, "Por favor corrige los errores señalados en el formulario.")

        context = {
            'pre_registros': pre_registros,
            'pre_registro_data': pre_registro_data, 
            'form': form, 
        }
        # Renderizamos de nuevo el paso 1 con los datos y errores
        return render(request, 'registros/registro_paso1.html', context)


class RegistroPaso2(View):
    def get(self, request):
        # Verificar si ya pasó por el paso 1
        if not request.session.get('registro_data'):
            logger.warning("Intento de acceso a paso 2 sin completar paso 1")
            messages.error(request, 'Primero debes completar el paso 1 del registro')
            return redirect('registro_paso1')
            
        # Si hay datos guardados en la sesión, los usamos para prellenar el formulario
        initial_data = request.session.get('fiador_data', {})
        form = RegistroFiadorForm(initial=initial_data)
        return render(request, 'registros/registro_paso2.html', {'form': form})
    
    def post(self, request):
        form = RegistroFiadorForm(request.POST)
        
        # Log para depuración
        logger.info(f"Datos del formulario fiador recibidos: {request.POST}")
        
        if form.is_valid():
            logger.info("Formulario de fiador válido, procesando...")            
            try:
                # Verificar si hay biblioteca seleccionada, usar la primera disponible si no hay
                biblioteca = form.cleaned_data.get('biblioteca')
                biblioteca_id = None
                
                if biblioteca:
                    biblioteca_id = biblioteca.id
                else:
                    # Intentar obtener la primera biblioteca disponible
                    primera_biblioteca = Biblioteca.objects.first()
                    if primera_biblioteca:
                        biblioteca_id = primera_biblioteca.id
                    else:
                        # Si no hay bibliotecas, mostrar error
                        messages.error(request, "No hay bibliotecas disponibles para el registro. Contacte al administrador.")
                        return render(request, 'registros/registro_paso1.html', {'form': form})
             
                # Guardamos los datos del formulario en la sesión
                fiador_data = {
                    'nombres': form.cleaned_data['nombres'],
                    'apellido_paterno': form.cleaned_data['apellido_paterno'],
                    'apellido_materno': form.cleaned_data['apellido_materno'],
                    'domicilio': form.cleaned_data['domicilio'],
                    'codigo_postal': form.cleaned_data.get('codigo_postal', ''),
                    'telefono': form.cleaned_data['telefono'],
                    'email': form.cleaned_data['email'],
                    'ocupacion': form.cleaned_data['ocupacion'],
                    'nombre_direccion_trabajo': form.cleaned_data['nombre_direccion_trabajo'],
                    'telefono_trabajo': form.cleaned_data['telefono_trabajo'],
                    'role': 'visitor',
                    'responsabilidad': True,
                    'retraso': 'No',
                    'suspension': 'No',
                    'aviso_usuario': 'No',
                    'biblioteca_id': biblioteca_id,
                }
                
                # Guardar en sesión
                request.session['fiador_data'] = fiador_data
                request.session.modified = True
                
                logger.info("Datos de fiador guardados en sesión. Redirigiendo a paso 3.")
                return redirect('registro_paso3')
            
            except Exception as e:
                logger.error(f"Error al guardar datos de fiador: {str(e)}")
                messages.error(request, f"Error al procesar el formulario: {str(e)}")
        else:
            # Log detallado de errores para depuración
            logger.error(f"Formulario de fiador inválido: {form.errors}")
            
            # Agregar mensajes de error específicos para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form[field].label if hasattr(form[field], 'label') else field
                    messages.error(request, f"Error en {field_label}: {error}")
        
        # Si llegamos aquí es porque hubo un error
        return render(request, 'registros/registro_paso2.html', {'form': form})

logger = logging.getLogger(__name__)

def registro_paso3(request):
    registro_data = request.session.get('registro_data', {})
    fiador_data = request.session.get('fiador_data', {})

    if request.method == 'POST':
        try:
            # Validaciones rápidas por si la sesión se perdió
            faltantes_reg = [k for k in ['username','email','password','nombres','apellido_paterno','edad','domicilio','codigo_postal','telefono','ocupacion','escuela_trabajo','telefono_escuela_trabajo','role'] if not registro_data.get(k)]
            faltantes_fia = [k for k in ['nombres','apellido_paterno','domicilio','telefono','email','ocupacion'] if not fiador_data.get(k)]
            if faltantes_reg or faltantes_fia:
                messages.error(request, "Faltan datos de registro o fiador. Regresa a los pasos anteriores.")
                return redirect('registro_paso2')

            logger.debug(f"Datos de registro: {registro_data}")
            logger.debug(f"Datos de fiador: {fiador_data}")

            with transaction.atomic():
                # Calcular fecha de vencimiento (2 años)
                hoy = date.today()
                try:
                    fecha_vencimiento = date(hoy.year + 2, hoy.month, hoy.day)
                except ValueError:
                    # Manejo de 29 de febrero, etc.
                    fecha_vencimiento = hoy + timedelta(days=730)

                # Obtener biblioteca
                from bibliotecas.models import Biblioteca
                biblioteca = Biblioteca.objects.first()
                if not biblioteca:
                    messages.error(request, "No hay bibliotecas disponibles para el registro.")
                    return redirect('registro_paso3')

                # 1) Crear el usuario
                registro = Registro.objects.create_user(
                    username=registro_data['username'],
                    email=registro_data['email'],
                    password=registro_data['password'],
                    nombres=registro_data['nombres'],
                    apellido_paterno=registro_data['apellido_paterno'],
                    apellido_materno=registro_data.get('apellido_materno', ''),
                    curp=registro_data.get('curp', ''),
                    edad=registro_data['edad'],
                    domicilio=registro_data['domicilio'],
                    codigo_postal=registro_data['codigo_postal'],
                    telefono=registro_data['telefono'],
                    ocupacion=registro_data['ocupacion'],
                    escuela_trabajo=registro_data['escuela_trabajo'],
                    telefono_escuela_trabajo=registro_data['telefono_escuela_trabajo'],
                    role=registro_data['role'],
                    fecha_vencimiento=fecha_vencimiento,
                    biblioteca_id=biblioteca.id
                )
                logger.debug(f"Registro creado con ID: {registro.id}")

                # 2) Crear (o actualizar) el fiador LIGADO al registro del usuario
                try:
                    Fiador.objects.create(
                        registro=registro,  # ← LIGAMOS AL USUARIO AQUÍ
                        nombres=fiador_data['nombres'],
                        apellido_paterno=fiador_data['apellido_paterno'],
                        apellido_materno=fiador_data.get('apellido_materno', ''),
                        domicilio=fiador_data['domicilio'],
                        codigo_postal=fiador_data.get('codigo_postal', ''),
                        telefono=fiador_data['telefono'],
                        email=fiador_data['email'],
                        ocupacion=fiador_data['ocupacion'],
                        nombre_direccion_trabajo=fiador_data.get('nombre_direccion_trabajo', ''),
                        telefono_trabajo=fiador_data.get('telefono_trabajo', ''),
                        role='visitor',
                        responsabilidad=True,
                        retraso='No',
                        suspension='No',
                        aviso_usuario='No',
                        biblioteca_id=biblioteca.id
                    )
                except IntegrityError:
                    # Si cambiaste a OneToOne y ya existía, actualiza
                    Fiador.objects.filter(registro=registro).update(
                        nombres=fiador_data['nombres'],
                        apellido_paterno=fiador_data['apellido_paterno'],
                        apellido_materno=fiador_data.get('apellido_materno', ''),
                        domicilio=fiador_data['domicilio'],
                        codigo_postal=fiador_data.get('codigo_postal', ''),
                        telefono=fiador_data['telefono'],
                        email=fiador_data['email'],
                        ocupacion=fiador_data['ocupacion'],
                        nombre_direccion_trabajo=fiador_data.get('nombre_direccion_trabajo', ''),
                        telefono_trabajo=fiador_data.get('telefono_trabajo', ''),
                        role='visitor',
                        responsabilidad=True,
                        retraso='No',
                        suspension='No',
                        aviso_usuario='No',
                        biblioteca_id=biblioteca.id
                    )

            # Limpiar sesión tras registro exitoso
            request.session.pop('registro_data', None)
            request.session.pop('fiador_data', None)

            messages.success(request, "¡Registro completado con éxito! Ya puedes iniciar sesión.")
            return redirect('/')

        except Exception as e:
            logger.error(f"Error en registro_paso3: {str(e)}", exc_info=True)
            messages.error(request, f"Error al registrar: {str(e)}")
            return redirect('registro_paso3')

    # GET
    return render(request, 'registros/registro_paso3.html', {
        'registro_data': registro_data,
        'fiador_data': fiador_data
    })


class RegistroCompletado(TemplateView):
    template_name = 'registros/registro_completado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.session.get('nuevo_usuario', {
            'username': 'Usuario', 
            'email': 'email@ejemplo.com'
        })
        
        # Limpiar los datos de la sesión después de mostrarlos
        if 'nuevo_usuario' in self.request.session:
            del self.request.session['nuevo_usuario']
            
        return context


    def get(self, request):
        # Usamos is_librarian_form=True para preconfigurar el formulario para bibliotecarios
        form = RegistroForm(is_librarian_form=True)
        return render(request, 'registros/agregar_bibliotecario.html', {'form': form})

    def post(self, request):
        # Pasamos is_librarian_form=True para asegurar que el formulario valide como bibliotecario
        form = RegistroForm(request.POST, is_librarian_form=True)
        if form.is_valid():
            try:
                # Verificar que el email no esté ya en uso
                email = form.cleaned_data['email']
                if User.objects.filter(email=email).exists():
                    form.add_error('email', 'Este correo electrónico ya está en uso')
                    messages.error(request, "Este correo electrónico ya está en uso")
                    return render(request, 'registros/agregar_bibliotecario.html', {'form': form})

                # Verificar que el username no esté ya en uso
                username = form.cleaned_data['username']
                if User.objects.filter(username=username).exists():
                    form.add_error('username', 'Este nombre de usuario ya está en uso')
                    messages.error(request, "Este nombre de usuario ya está en uso")
                    return render(request, 'registros/agregar_bibliotecario.html', {'form': form})

                # Usar el método create_librarian para crear el usuario con is_staff=True
                bibliotecario = User.objects.create_librarian(
                    email=email,
                    username=username,
                    password=form.cleaned_data['password'],
                    nombres=form.cleaned_data['nombres'],
                    apellido_paterno=form.cleaned_data['apellido_paterno'],
                    apellido_materno=form.cleaned_data['apellido_materno'],
                    edad=form.cleaned_data.get('edad'),
                    domicilio=form.cleaned_data.get('domicilio', ''),
                    codigo_postal=form.cleaned_data.get('codigo_postal', ''),
                    telefono=form.cleaned_data.get('telefono', ''),
                    ocupacion=form.cleaned_data.get('ocupacion', ''),
                    escuela_trabajo=form.cleaned_data.get('escuela_trabajo', ''),
                    telefono_escuela_trabajo=form.cleaned_data.get('telefono_escuela_trabajo', ''),
                    biblioteca=form.cleaned_data.get('biblioteca'),
                    is_active=form.cleaned_data.get('is_active', True),
                    fecha_vencimiento=date.today() + timedelta(days=365*2)
                )

                messages.success(request, "¡Bibliotecario registrado con éxito!")
                return redirect('user_list')  # Asegúrate de que esta URL esté definida

            except Exception as e:
                logger.error(f"Error al registrar bibliotecario: {str(e)}")
                messages.error(request, f"Error al registrar el bibliotecario: {str(e)}")
        else:
            # Mostrar errores específicos del formulario
            for field_name, error_list in form.errors.items():
                for error in error_list:
                    field_label = form[field_name].label if hasattr(form[field_name], 'label') else field_name
                    messages.error(request, f"Error en {field_label}: {error}")
            messages.error(request, "Por favor corrige los errores señalados en el formulario.")

        return render(request, 'registros/agregar_bibliotecario.html', {'form': form})