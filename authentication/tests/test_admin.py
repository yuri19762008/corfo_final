# authentication/tests/test_admin.py

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from authentication.admin import UserAdmin
from authentication.models import User
from authentication.tests.factories import UserFactory
from authorization.models import ProfileTypes, ProfileType

class MockRequest:
    pass

class UserAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = AdminSite()
        self.user_admin = UserAdmin(User, self.admin_site)

    def test_save_model_applies_permissions(self):
        # Crear tipo de perfil y usuario sin permisos
        profile = ProfileType.objects.create(type=ProfileTypes.ADMINISTRADOR_SMA, name="Administrador SMA")
        user = UserFactory(profile_type=profile)

        # Simular guardado desde el admin
        form = None  # no se usa en nuestro método
        change = False
        request = self.factory.get("/admin/authentication/user/add/")

        self.user_admin.save_model(request, user, form, change)

        # Verificamos que se le asignaron permisos
        self.assertTrue(user.user_permissions.exists() or user.is_staff)