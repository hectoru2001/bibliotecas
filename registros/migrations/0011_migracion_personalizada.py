from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('registros', '0010_registro_groups_registro_user_permissions_and_more'),
        ('admin', '0003_logentry_add_action_flag_choices'),
    ]

    operations = [
        # Para SQLite, omitimos la adición de la restricción ya que no es soportada directamente
        migrations.RunSQL(
            sql="SELECT 1;",  # Un comando vacío que no hace nada
            reverse_sql="SELECT 1;",
            state_operations=[
                # Esto asegura que el estado de la migración se actualice
                migrations.RunPython(
                    code=lambda apps, schema_editor: None,
                    reverse_code=lambda apps, schema_editor: None,
                ),
            ],
        ),
    ]