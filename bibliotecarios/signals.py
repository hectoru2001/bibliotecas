# bibliotecarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Bibliotecario

ROLE_MAP = {
    "admin_system": "AdminSistema",
    "admin_biblioteca": "AdminBiblioteca",
    "librarian": "Bibliotecario",
    "guest": "Invitado",
}

@receiver(post_save, sender=Bibliotecario)
def sync_user_group(sender, instance, created, **kwargs):
    user = getattr(instance, 'user', None)
    if not user:
        return

    # permite el acceso al panel
    if not user.is_staff:
        user.is_staff = True
        user.save(update_fields=["is_staff"])

    role_value = getattr(user, 'role', None)  # p.ej. 'librarian'
    group_name = ROLE_MAP.get(role_value, "Bibliotecario")
    group, _ = Group.objects.get_or_create(name=group_name)

    # asigna el grupo (un solo rol por simplicidad)
    user.groups.clear()
    user.groups.add(group)
