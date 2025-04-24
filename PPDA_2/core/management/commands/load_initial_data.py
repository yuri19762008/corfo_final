import io
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.timezone import now
from django.apps import apps
import json

from authentication.models import User
from authorization.utils import apply_permissions_based_on_profile

def cargar_fixture_como_objetos(path_fixture):
    """
    Carga un archivo JSON tipo fixture y crea las instancias del modelo usando .save(),
    respetando validaciones, auto_now_add y relaciones ForeignKey/M2M.
    """
    with open(path_fixture, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for obj in data:
        model_label = obj["model"]  # e.g. "core.organismo"
        model = apps.get_model(model_label)
        fields = obj["fields"]

        m2m_fields = {}
        fk_fields = {}

        # Separamos campos M2M y FK
        for field in list(fields.keys()):
            field_object = model._meta.get_field(field)
            if field_object.many_to_many:
                m2m_fields[field] = fields.pop(field)
            elif field_object.many_to_one or field_object.one_to_one:
                fk_model = field_object.related_model
                pk = fields[field]
                try:
                    fields[field] = fk_model.objects.get(pk=pk)
                except fk_model.DoesNotExist:
                    raise ValueError(f"No se encontró instancia de {fk_model.__name__} con pk={pk}")

        instance, created = model.objects.update_or_create(
            defaults=obj["fields"],
            **{model._meta.pk.name: obj["pk"]}
        ) # Activa .save() y auto_now_add

        # Asignar relaciones M2M después de guardar
        for field_name, pks in m2m_fields.items():
            m2m_manager = getattr(instance, field_name)
            m2m_manager.set(pks)


class Command(BaseCommand):
    """
    Comando personalizado para:
    - Cargar fixtures del sistema
    - Aplicar permisos a usuarios según su profile_type
    - Asignar timestamps de creación/modificación automáticamente si no están definidos
    """

    help = 'Carga fixtures iniciales y aplica permisos y timestamps automáticamente'

    def handle(self, *args, **kwargs):
        fixtures = [
            'authorization/fixtures/profiletype.json',
            'authentication/fixtures/users.json',
            'core/fixtures/organismos_sectoriales.json',
            'core/fixtures/tipo_medidas.json',
            'core/fixtures/medidas.json',
            'core/fixtures/planes_descontaminacion.json',
        ]

        self.stdout.write("📦 Cargando fixtures...")
        for fixture in fixtures:
            try:
                self.stdout.write(f"📂 Cargando {fixture}...")
                cargar_fixture_como_objetos(fixture)
                self.stdout.write(self.style.SUCCESS(f"✔ {fixture} cargado correctamente"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error al cargar {fixture}: {e}"))

        self.stdout.write("🔐 Aplicando permisos a usuarios...")
        for user in User.objects.all():
            apply_permissions_based_on_profile(user)
            user.save()
        self.stdout.write(self.style.SUCCESS("✔ Permisos aplicados correctamente a todos los usuarios."))

        self.stdout.write("⏱️ Asignando timestamps automáticamente...")
        self.asignar_timestamps_a_modelos()
        self.stdout.write(self.style.SUCCESS("✔ Timestamps asignados correctamente."))

    def asignar_timestamps_a_modelos(self):
        """
        Recorre todas las apps y modelos, y si detecta campos `fecha_creacion` o `fecha_modificacion`,
        los asigna si están vacíos.
        """
        total_actualizados = 0

        for model in apps.get_models():
            campos = model._meta.get_fields()
            tiene_fecha_creacion = any(f.name == "fecha_creacion" for f in campos)
            tiene_fecha_modificacion = any(f.name == "fecha_modificacion" for f in campos)

            if not (tiene_fecha_creacion or tiene_fecha_modificacion):
                continue  # Saltamos modelos que no tienen esas fechas

            for obj in model.objects.all():
                actualizado = False
                if tiene_fecha_creacion and not getattr(obj, "fecha_creacion", None):
                    setattr(obj, "fecha_creacion", now())
                    actualizado = True
                if tiene_fecha_modificacion and not getattr(obj, "fecha_modificacion", None):
                    setattr(obj, "fecha_modificacion", now())
                    actualizado = True
                if actualizado:
                    obj.save()
                    total_actualizados += 1

        self.stdout.write(f"🛠️ Total de objetos actualizados con timestamps: {total_actualizados}")