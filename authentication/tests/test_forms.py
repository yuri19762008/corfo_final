# authentication/tests/test_forms.py
from django.test import TestCase
from authentication.forms import UserCreationForm, UserChangeForm
from authentication.models import User
from authorization.models import ProfileType, ProfileTypes



class UserCreationFormTest(TestCase):
    def setUp(self):
        self.profile_type = ProfileType.objects.create(
            type=ProfileTypes.ADMINISTRADOR_SMA,
            name="Administrador SMA"
        )

    def test_passwords_do_not_match(self):
        form_data = {
            'email': 'mismatch@test.com',
            'first_name': 'Test',
            'last_name': 'Mismatch',
            'profile_type': self.profile_type.id,
            'password1': 'pass1234',
            'password2': 'differentpass',
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Las contraseñas no coinciden.", form.errors["password2"])

    def test_valid_form_creates_user(self):
        form_data = {
            'email': 'newuser@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'profile_type': self.profile_type.id,
            'password1': 'securepass123',
            'password2': 'securepass123',
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "newuser@test.com")
        self.assertTrue(user.check_password("securepass123"))

class UserChangeFormTest(TestCase):
    def setUp(self):
        self.profile_type = ProfileType.objects.create(
            type=ProfileTypes.ANALISTA_SMA,
            name="Analista SMA"
        )
        self.user = User.objects.create_user(
            email="change@test.com",
            first_name="Change",
            last_name="Test",
            profile_type=self.profile_type,
            password="changepass"
        )

    def test_clean_password_returns_initial(self):
        form = UserChangeForm(instance=self.user)
        self.assertEqual(form.clean_password(), self.user.password)