# tests/test_load_initial_data.py

from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from authorization.models import ProfileType
from authentication.models import User

class LoadInitialDataCommandTest(TestCase):

    def test_load_initial_data_command(self):
        out = StringIO()
        call_command('load_initial_data', stdout=out)

        output = out.getvalue()
        self.assertIn("authorization/fixtures/profiletype.json", output)
        self.assertIn("authentication/fixtures/users.json", output)
        self.assertIn("✔", output)

        # Validaciones mínimas esperadas post carga
        self.assertTrue(ProfileType.objects.exists())
        self.assertTrue(User.objects.exists())