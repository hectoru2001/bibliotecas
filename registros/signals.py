# projects/registros/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Registro  # tu user model
from bibliotecarios.models import Bibliotecario

@receiver(post_save, sender=Registro)
def ensure_bibliotecario_profile_and_perms(sender, instance: Registro, created, **kwargs):

    user = instance
    if getattr(user, 'role', '') != 'librarian' or not user.is_active:
        return

    # 1) staff sin recursión
    if not user.is_staff:
        # Evita re-disparar señales con save(); usa update()
        sender.objects.filter(pk=user.pk).update(is_staff=True)
        user.is_staff = True  # refleja en memoria

    # 2) grupo Bibliotecario
    group, _ = Group.objects.get_or_create(name='Bibliotecario')
    if not user.groups.filter(id=group.id).exists():
        user.groups.add(group)

    # 3) perfil Bibliotecario
    defaults = {
        'nombre': getattr(user, 'nombres', '') or user.username,
        'apellido': getattr(user, 'apellido_paterno', '') or '',
        'email': user.email or '',
        'telefono': getattr(user, 'telefono', '') or '',
        'direccion': getattr(user, 'direccion', '') or '',
        'biblioteca': getattr(user, 'biblioteca', None),
        'active': True,
    }
    biblio, created_b = Bibliotecario.objects.get_or_create(user=user, defaults=defaults)

    # Mantén la biblioteca sincronizada si cambia en el usuario
    if getattr(user, 'biblioteca_id', None) and biblio.biblioteca_id != user.biblioteca_id:
        biblio.biblioteca_id = user.biblioteca_id
        biblio.save(update_fields=['biblioteca', 'active'])
