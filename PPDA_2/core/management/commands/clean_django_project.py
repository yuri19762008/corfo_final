from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import shutil
import subprocess


def get_current_git_branch():
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return None


class Command(BaseCommand):
    """
    Comando personalizado para limpiar el proyecto Django de forma segura.

    ✅ Este script realiza:
    1. Eliminación de la base de datos `db.sqlite3`
    2. Limpieza de migraciones en apps locales (excepto `__init__.py`)
    3. Eliminación de archivos `.pyc` y carpetas `__pycache__` en todo el proyecto

    🛡️ Protege las ramas `main` y `development` de la eliminación de migraciones.

    📝 Requiere que `settings.LOCAL_APPS` esté definido.
    """

    help = '🧹 Limpia base de datos, migraciones, archivos .pyc y __pycache__ de todo el proyecto.'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        # Detectar la rama actual
        branch = get_current_git_branch()
        if branch in ['main', 'development']:
            self.stdout.write(self.style.ERROR(f'🚫 Estás en la rama protegida "{branch}", no se limpiarán las migraciones.'))
            self.stdout.write(self.style.NOTICE('👉 Cambia a una rama de feature si deseas ejecutar limpieza completa.'))
            return

        # Paso 1: Eliminar la base de datos SQLite
        db_path = base_dir / 'db.sqlite3'
        if db_path.exists():
            db_path.unlink()
            self.stdout.write(self.style.SUCCESS(f'🗑  Base de datos eliminada: {db_path}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  No se encontró db.sqlite3, nada que eliminar.'))

        # Paso 2: Eliminar migraciones en apps locales
        try:
            local_apps = settings.LOCAL_APPS
        except AttributeError:
            self.stdout.write(self.style.ERROR("❌ No se encontró la variable LOCAL_APPS en settings.py"))
            return

        self.stdout.write('\n📦 Limpiando migraciones en apps locales...\n')
        for app in local_apps:
            migrations_dir = base_dir / app / 'migrations'
            if migrations_dir.exists():
                deleted = 0
                for item in migrations_dir.iterdir():
                    if item.name != '__init__.py':
                        if item.is_file():
                            item.unlink()
                            deleted += 1
                        elif item.is_dir() and item.name == '__pycache__':
                            shutil.rmtree(item)
                            deleted += 1
                self.stdout.write(self.style.SUCCESS(f'✔ Migraciones limpiadas en: {app} ({deleted} ítems)'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  No se encontró carpeta de migraciones en: {app}'))

        # Paso 3: Eliminar __pycache__ y archivos .pyc en todo el proyecto
        self.stdout.write('\n🧹 Limpiando __pycache__/ y archivos .pyc en todo el proyecto...\n')

        pyc_count = 0
        cache_dirs = []

        for path in base_dir.rglob('*'):
            if path.is_file() and path.suffix == '.pyc':
                path.unlink()
                pyc_count += 1
            elif path.is_dir() and path.name == '__pycache__':
                shutil.rmtree(path)
                cache_dirs.append(str(path.relative_to(base_dir)))

        self.stdout.write(self.style.SUCCESS(f'✔ Archivos .pyc eliminados: {pyc_count}'))
        self.stdout.write(self.style.SUCCESS(f'✔ Carpetas __pycache__ eliminadas: {len(cache_dirs)}'))

        if cache_dirs:
            for dir_name in cache_dirs:
                self.stdout.write(f'   🧹 {dir_name}/')

        self.stdout.write(self.style.SUCCESS('\n✅ Limpieza completa. Todo listo para regenerar migraciones.'))
        self.stdout.write(self.style.NOTICE("➡️ Ejecuta ahora 'python manage.py makemigrations && python manage.py migrate'"))