from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bibliotecarios.models import Bibliotecario

ROLES = {
    "AdminSistema":     ["view_bibliotecario", "add_bibliotecario", "change_bibliotecario", "delete_bibliotecario"],
    "AdminBiblioteca":  ["view_bibliotecario", "add_bibliotecario", "change_bibliotecario"],
    "Bibliotecario":    ["view_bibliotecario"],
    "Invitado":         [],
}

class Command(BaseCommand):  # ¡Ojo! Debe llamarse Command, no BaseCommand
    help = "Crea/actualiza grupos de roles y asigna permisos del modelo Bibliotecario"

    def handle(self, *args, **options):
        # Asegúrate de que el modelo ya está migrado para que existan sus permisos nativos
        ct = ContentType.objects.get_for_model(Bibliotecario)

        for role, codenames in ROLES.items():
            group, _ = Group.objects.get_or_create(name=role)
            group.permissions.clear()  # opcional: limpia antes de reasignar

            for codename in codenames:
                try:
                    perm = Permission.objects.get(content_type=ct, codename=codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stderr.write(f"[WARN] Permiso no encontrado: {codename}")

            self.stdout.write(self.style.SUCCESS(f"Grupo '{role}' configurado."))
        self.stdout.write(self.style.SUCCESS("Listo."))
