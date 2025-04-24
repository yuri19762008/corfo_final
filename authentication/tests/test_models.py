# authentication/tests/test_models.py
from django.test import TestCase
from authentication.models import User, UserManager
from authorization.models import ProfileType, ProfileTypes
from .factories import ProfileTypeFactory




class UserManagerTestCase(TestCase):
    def test_create_user_directly(self):
        profile_type = ProfileTypeFactory(type=ProfileTypes.ADMINISTRADOR_SMA)

        user = User.objects.create_user(
            email="direct@test.com",
            first_name="Directo",
            last_name="Test",
            profile_type=profile_type,
            password="testpass123"
        )
        

        self.assertEqual(user.email, "direct@test.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.profile_type, profile_type)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_directly(self):
        ProfileType.objects.create(
            type=ProfileTypes.ADMINISTRADOR_SISTEMA,
            name="Administrador de Sistema"
        )

        user = User.objects.create_superuser(
            email="super@test.com",
            first_name="Super",
            last_name="User",
            password="adminpass123",
        )

        self.assertEqual(user.email, "super@test.com")
        self.assertTrue(user.check_password("adminpass123"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.profile_type.type, ProfileTypes.ADMINISTRADOR_SISTEMA)


class UserModelTestCase(TestCase):
    def setUp(self):
        self.profile_type = ProfileType.objects.create(
            type=ProfileTypes.ANALISTA_SMA,
            name="Analista SMA"
        )

    def test_create_user_with_instance(self):
        user = User.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="securepass",
            profile_type=self.profile_type
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepass"))
        self.assertEqual(user.profile_type, self.profile_type)

    def test_create_user_with_id(self):
        user = User.objects.create_user(
            email="test2@example.com",
            first_name="ID",
            last_name="Based",
            password="securepass",
            profile_type=self.profile_type.id
        )
        self.assertEqual(user.profile_type, self.profile_type)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                first_name="Sin",
                last_name="Correo",
                password="securepass",
                profile_type=self.profile_type
            )

    def test_create_user_with_invalid_profile_type_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="error@example.com",
                first_name="Bad",
                last_name="Profile",
                password="securepass",
                profile_type="invalido"
            )

    def test_create_superuser_has_correct_flags(self):
        admin_profile = ProfileType.objects.create(
            type=ProfileTypes.ADMINISTRADOR_SISTEMA,
            name="Admin Sistema"
        )
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            first_name="Super",
            last_name="User",
            password="securepass"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_missing_flags_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="fail@example.com",
                first_name="Bad",
                last_name="Flags",
                password="pass",
                is_staff=False
            )

    def test_str_and_full_name_methods(self):
        user = User.objects.create_user(
            email="name@example.com",
            first_name="Nombre",
            last_name="Apellido",
            password="pass",
            profile_type=self.profile_type
        )
        self.assertEqual(str(user), "Nombre Apellido")
        self.assertEqual(user.get_full_name(), "Nombre Apellido")

    def test_password_is_hashed_on_save(self):
        user = User(
            email="hash@example.com",
            first_name="Hash",
            last_name="Test",
            password="rawpass",
            profile_type=self.profile_type
        )
        user.save()
        self.assertNotEqual(user.password, "rawpass")
        self.assertTrue(user.password.startswith("pbkdf2_"))

    def test_create_user_with_invalid_profile_type_id_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email="invalid@test.com",
                first_name="Nombre",
                last_name="Apellido",
                password="securepass",
                profile_type=99999  # ID que no existe
            )
        self.assertIn("tipo de perfil indicado no existe", str(context.exception))

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email="failsuper@test.com",
                first_name="Fake",
                last_name="Admin",
                password="adminpass",
                is_superuser=False  # 👈 esto dispara la línea 44
            )
        self.assertIn("superusuario debe tener is_superuser=True", str(context.exception))