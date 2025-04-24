from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection
from authorization.utils import setup_groups

@receiver(post_migrate)
def create_groups_after_migration(sender, **kwargs):
    """
    Crea los grupos y sus permisos después de aplicar las migraciones.

    ⚠️ Solo se ejecuta si:
        - La app 'authorization' acaba de migrar
        - Ya existe la tabla 'auth_group' (evita errores si la DB es nueva)

    Esto permite levantar el sistema desde cero sin fallar al aplicar migrate.
    """
    if sender.label != 'authorization':
        return

    # Verifica que exista la tabla auth_group antes de usarla
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='auth_group';"
        )
        if cursor.fetchone():
            setup_groups()