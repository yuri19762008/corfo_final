# authentication/tests/test_endpoints.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import ProfileTypes, User
from authentication.tests.factories import  user_admin_sistema, user_admin_sma,user_analista_sma,user_funcionario_sectorial
from authorization.tests.factories import ProfileTypeFactory

class RefreshTokenTestCase(APITestCase):
    def setUp(self):
        self.user = user_admin_sistema()
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)

    def test_refresh_token_returns_new_access(self):
        response = self.client.post(reverse('token_refresh'), {
            'refresh': self.refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(reverse('token_refresh'), {
            'refresh': 'token_invalido'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

class LogoutTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user_admin_sistema()
        refresh = RefreshToken.for_user(cls.user)
        cls.refresh_token = str(refresh)

    def test_logout_successful(self):
        response = self.client.post(reverse('logout'), {
            'refresh_token': self.refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["message"], "Cierre de Sesión Exitoso!.")

    def test_logout_invalid_token(self):
        response = self.client.post(reverse('logout'), {
            'refresh_token': "token_invalido"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_logout_no_token_provided(self):
        response = self.client.post(reverse('logout'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class LoginTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'securepass123'
        cls.admin_sistema = user_admin_sistema()
        cls.admin_sma = user_admin_sma()
        cls.analista_sma = user_analista_sma()
        cls.funcionario = user_funcionario_sectorial()

        for user in [cls.admin_sistema, cls.admin_sma, cls.analista_sma, cls.funcionario]:
            user.set_password(cls.password)
            user.save()

    def perform_login(self, email, password):
        return self.client.post(reverse('login'), {
            'email': email,
            'password': password
        })

    def assert_valid_login(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_admin_sistema(self):
        response = self.perform_login(self.admin_sistema.email, self.password)
        self.assert_valid_login(response)

    def test_login_admin_sma(self):
        response = self.perform_login(self.admin_sma.email, self.password)
        self.assert_valid_login(response)

    def test_login_analista_sma(self):
        response = self.perform_login(self.analista_sma.email, self.password)
        self.assert_valid_login(response)

    def test_login_funcionario_sectorial(self):
        response = self.perform_login(self.funcionario.email, self.password)
        self.assert_valid_login(response)

    def test_login_invalid_credentials(self):
        response = self.perform_login(self.admin_sistema.email, 'wrongpassword')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_token_contains_user_data(self):
        response = self.perform_login(self.admin_sistema.email, self.password)
        self.assertEqual(response.data['email'], self.admin_sistema.email)
        self.assertIn('full_name', response.data)

class RegisterUserTestCase(APITestCase):

    def perform_register(self, profile_type_enum, email="funcionario@correo.com"):
        profile_type = ProfileTypeFactory(type=profile_type_enum)
        data = {
            "email": email,
            "first_name": "Funcionario",
            "last_name": "Prueba",
            "password": "funcionario123",
            "profile_type": profile_type.id,
        }
        return self.client.post(reverse("register"), data), profile_type

    def setUp(self):
        self.admin = user_admin_sistema()
        self.client.force_authenticate(user=self.admin)

    def test_register_administrador_sistema(self):
        response, profile_type = self.perform_register(ProfileTypes.ADMINISTRADOR_SISTEMA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="funcionario@correo.com")
        self.assertEqual(user.profile_type, profile_type)
        self.assertTrue(user.is_staff)         # porque es administrador_sma
        self.assertTrue(user.is_superuser)    # solo admin_sistema lo es

    def test_register_administrador_sma(self):
        response, profile_type = self.perform_register(ProfileTypes.ADMINISTRADOR_SMA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="funcionario@correo.com")
        self.assertEqual(user.profile_type, profile_type)
        self.assertTrue(user.is_staff)         # porque es administrador_sma
        self.assertFalse(user.is_superuser)    # solo admin_sistema lo es


    def test_register_analista_sma(self):
        response, profile_type = self.perform_register(ProfileTypes.ANALISTA_SMA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="funcionario@correo.com")
        self.assertEqual(user.profile_type, profile_type)
        self.assertFalse(user.is_staff)         
        self.assertFalse(user.is_superuser) 
        

    def test_register_funcionario_sectorial(self):
        response, profile_type = self.perform_register(ProfileTypes.FUNCIONARIO_SECTORIAL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="funcionario@correo.com")
        self.assertEqual(user.profile_type, profile_type)
        self.assertFalse(user.is_staff)         
        self.assertFalse(user.is_superuser)

    def test_register_email_duplicado(self):
        profile_type = ProfileTypeFactory(type=ProfileTypes.FUNCIONARIO_SECTORIAL)
        # Crear un usuario con ese email
        User.objects.create_user(
            email="repetido@correo.com",
            first_name="Usuario",
            last_name="Uno",
            password="passwordseguro123",
            profile_type=profile_type,
        )
        # Intentar registrar otro con el mismo correo
        data = {
            "email": "repetido@correo.com",
            "first_name": "Usuario",
            "last_name": "Dos",
            "password": "passwordseguro123",
            "profile_type": profile_type.id,
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_nombre_vacio(self):
        profile_type = ProfileTypeFactory(type=ProfileTypes.FUNCIONARIO_SECTORIAL)
        data = {
            "email": "nuevo@correo.com",
            "first_name": "   ",  # Nombre vacío con espacios
            "last_name": "Apellido",
            "password": "contraseñaSegura123",
            "profile_type": profile_type.id,
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)

    def test_register_password_corta(self):
        profile_type = ProfileTypeFactory(type=ProfileTypes.FUNCIONARIO_SECTORIAL)
        data = {
            "email": "nuevo@correo.com",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "password": "123",  # Demasiado corta
            "profile_type": profile_type.id,
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)