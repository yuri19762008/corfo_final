"""
Tests para verificar la correcta asignación de permisos según el tipo de perfil (ProfileType).

Cada usuario debe recibir exactamente los permisos que corresponden a su tipo de perfil, y este archivo se encarga de garantizar eso.
"""
from django.test import TestCase
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.models import ContentType
from authentication.tests.factories import UserFactory
from authorization.tests.factories import ProfileTypeFactory
from authorization.models import ProfileTypes
from authorization.utils import PERMISSIONS_BY_PROFILE_TYPE, setup_groups, apply_permissions_based_on_profile

import logging
logger = logging.getLogger(__name__)

class ProfilePermissionsTest(TestCase):
    """
    Tests para verificar que cada usuario tenga exactamente los permisos correspondientes a su tipo de perfil.

    Incluye:
    - Validación de permisos exactos para cada tipo de perfil.
    - Manejo de errores cuando se solicitan permisos inexistentes.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Prepara los permisos y grupos antes de ejecutar los tests.

        - Fuerza la creación de ContentTypes y permisos para todos los modelos.
        - Llama a `setup_groups()` para asegurar que los grupos y sus permisos estén configurados.
        """
        for app_config in apps.get_app_configs():
            ContentType.objects.get_for_models(*app_config.get_models())  # Fuerza creación de ContentTypes
            create_permissions(app_config, verbosity=0)  # Fuerza creación de permisos

        setup_groups()

    def assertUserHasExactlyThesePermissions(self, user, expected_codenames):
        """
        Compara los permisos reales del usuario con los esperados.
        Permisos esperados se dan como codenames (sin prefijo de app).

        Args:
            user (User): Usuario a evaluar.
            expected_codenames (list[str]): Lista de codenames esperados (ej. 'view_reporte').

        Lanza un `fail()` si algún permiso no existe o si hay diferencia con los permisos reales.
        """
        user_permissions = set(user.get_all_permissions())
        expected_permissions = set()

        for codename in expected_codenames:
            matches = Permission.objects.filter(codename=codename)
            if not matches.exists():
                self.fail(f"⚠️ Permiso con codename '{codename}' no existe en ninguna app.")
            for perm in matches:
                expected_permissions.add(f"{perm.content_type.app_label}.{perm.codename}")

        self.assertSetEqual(user_permissions, expected_permissions)

    def test_permiso_inexistente_lanza_fail(self):
        """
        Valida que se lance un error si se busca un permiso que no existe.
        """
        user = UserFactory()
        with self.assertRaises(AssertionError):
            self.assertUserHasExactlyThesePermissions(user, ["permiso_falso_inexistente"])

    def create_and_check_user(self, profile_type_key):
        """
        Crea un usuario con un tipo de perfil y valida que reciba los permisos esperados.

        Args:
            profile_type_key (str): Uno de los valores de `ProfileTypes` (enum).
        """
        profile = ProfileTypeFactory(type=profile_type_key)
        user = UserFactory(profile_type=profile)
        apply_permissions_based_on_profile(user)

        if PERMISSIONS_BY_PROFILE_TYPE[profile_type_key] == '__all__':
            expected = Permission.objects.all().values_list('codename', flat=True)
        else:
            expected = PERMISSIONS_BY_PROFILE_TYPE[profile_type_key]

        self.assertUserHasExactlyThesePermissions(user, expected)

    def test_admin_sistema_permissions(self):
        """Verifica los permisos asignados al perfil ADMINISTRADOR_SISTEMA."""
        self.create_and_check_user(ProfileTypes.ADMINISTRADOR_SISTEMA)

    def test_admin_sma_permissions(self):
        """Verifica los permisos asignados al perfil ADMINISTRADOR_SMA."""
        self.create_and_check_user(ProfileTypes.ADMINISTRADOR_SMA)

    def test_analista_sma_permissions(self):
        """Verifica los permisos asignados al perfil ANALISTA_SMA."""
        self.create_and_check_user(ProfileTypes.ANALISTA_SMA)

    def test_funcionario_sectorial_permissions(self):
        """Verifica los permisos asignados al perfil FUNCIONARIO_SECTORIAL."""
        self.create_and_check_user(ProfileTypes.FUNCIONARIO_SECTORIAL)