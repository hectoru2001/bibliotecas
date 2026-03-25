import os
import django
import sys

# Añadir el directorio del proyecto al path
sys.path.append("c:\\Users\\USUARIO\\Documents\\BiblioWeb_projects_v05")

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')
django.setup()

# Importa tus modelos
from django.contrib.admin.models import LogEntry
try:
    from bibliotecas.models import Biblioteca
    from bibliotecarios.models import Bibliotecario
    from registros.models import Registro
    from fiadores.models import Fiador
    from libros.models import Libro, CopiaLibro
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)

def clean_database(current_user_id):
    # Guarda el usuario actual
    try:
        if current_user_id:
            current_user = Registro.objects.get(id=current_user_id)
            print(f"Manteniendo usuario: {current_user.email}")
        else:
            current_user = None
    except Registro.DoesNotExist:
        print(f"Usuario con ID {current_user_id} no encontrado. Continuando sin preservar usuario.")
        current_user = None

    # Elimina registros relacionados en orden para evitar violaciones de clave foránea
    print("Eliminando entradas de log del admin...")
    LogEntry.objects.all().delete()
    
    print("Eliminando fiadores...")
    Fiador.objects.all().delete()
    
    print("Eliminando copias de libros...")
    try:
        CopiaLibro.objects.all().delete()
    except Exception as e:
        print(f"Error al eliminar copias de libros: {e}")
    
    print("Eliminando libros...")
    try:
        Libro.objects.all().delete()
    except Exception as e:
        print(f"Error al eliminar libros: {e}")
    
    print("Eliminando bibliotecarios...")
    try:
        Bibliotecario.objects.all().delete()
    except Exception as e:
        print(f"Error al eliminar bibliotecarios: {e}")
    
    print("Eliminando bibliotecas...")
    try:
        Biblioteca.objects.all().delete()
    except Exception as e:
        print(f"Error al eliminar bibliotecas: {e}")
    
    # Elimina todos los usuarios excepto el actual
    if current_user:
        print(f"Eliminando usuarios excepto ID {current_user_id}...")
        try:
            Registro.objects.exclude(id=current_user_id).delete()
        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")
    else:
        print("Eliminando todos los usuarios...")
        try:
            Registro.objects.all().delete()
        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")
    
    print("¡Limpieza completada!")

if __name__ == "__main__":
    # Pide el ID del usuario a conservar
    try:
        user_id = input("Introduce el ID del usuario que deseas conservar (deja en blanco para eliminar todos): ")
    
        if user_id.strip():
            clean_database(int(user_id))
        else:
            clean_database(None)
    except Exception as e:
        print(f"Error inesperado: {e}")