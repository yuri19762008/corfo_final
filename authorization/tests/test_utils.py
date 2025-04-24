# authorization/tests/test_utils.py
from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from authorization.utils import apply_permissions_based_on_profile, get_permissions_for_profile_type
from authentication.tests.factories import UserFactory
from authorization.tests.factories import ProfileTypeFactory
from authorization.models import ProfileTypes
from authorization.utils import PERMISSIONS_BY_PROFILE_TYPE

class GetPermissionsForProfileTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for app_config in apps.get_app_configs():
            create_permissions(app_config, verbosity=0)

    def assertHasCodenames(self, result_queryset, expected_codenames):
        result_codenames = set(result_queryset.values_list('codename', flat=True))
        self.assertEqual(result_codenames, set(expected_codenames))

    def test_admin_sistema_gets_all_permissions(self):
        expected = Permission.objects.all()
        result = get_permissions_for_profile_type(ProfileTypes.ADMINISTRADOR_SISTEMA)
        self.assertCountEqual(result, expected)

    def test_admin_sma_permissions(self):
        expected = PERMISSIONS_BY_PROFILE_TYPE[ProfileTypes.ADMINISTRADOR_SMA]
        result = get_permissions_for_profile_type(ProfileTypes.ADMINISTRADOR_SMA)
        self.assertHasCodenames(result, expected)

    def test_analista_sma_permissions(self):
        expected = PERMISSIONS_BY_PROFILE_TYPE[ProfileTypes.ANALISTA_SMA]
        result = get_permissions_for_profile_type(ProfileTypes.ANALISTA_SMA)
        self.assertHasCodenames(result, expected)

    def test_funcionario_sectorial_permissions(self):
        expected = PERMISSIONS_BY_PROFILE_TYPE[ProfileTypes.FUNCIONARIO_SECTORIAL]
        result = get_permissions_for_profile_type(ProfileTypes.FUNCIONARIO_SECTORIAL)
        self.assertHasCodenames(result, expected)

    def test_invalid_profile_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_permissions_for_profile_type("perfil_falso")

    def test_apply_permissions_sin_grupo_asignado(self):
        # Creamos un ProfileType que no tenga grupo asociado
        custom_type = ProfileTypeFactory(type="CUSTOM_ROLE")
        user = UserFactory(profile_type=custom_type)

        # No llamamos a setup_groups(), por lo tanto no existe el grupo "CUSTOM_ROLE"
        apply_permissions_based_on_profile(user)

        # El usuario no debería tener ningún grupo asignado
        self.assertEqual(user.groups.count(), 0)

class ApplyPermissionsTestCase(TestCase):
    def test_admin_sistema_permissions(self):
        profile = ProfileTypeFactory(type=ProfileTypes.ADMINISTRADOR_SISTEMA)
        user = UserFactory(profile_type=profile)
        apply_permissions_based_on_profile(user)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_admin_sma_permissions(self):
        profile = ProfileTypeFactory(type=ProfileTypes.ADMINISTRADOR_SMA)
        user = UserFactory(profile_type=profile)
        apply_permissions_based_on_profile(user)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_analista_permissions(self):
        profile = ProfileTypeFactory(type=ProfileTypes.ANALISTA_SMA)
        user = UserFactory(profile_type=profile)
        apply_permissions_based_on_profile(user)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_funcionario_sectorial(self):
        profile = ProfileTypeFactory(type=ProfileTypes.FUNCIONARIO_SECTORIAL)
        user = UserFactory(profile_type=profile)
        apply_permissions_based_on_profile(user)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)