# authorization/tests/test_models.py

from django.test import TestCase
from authorization.models import ProfileType, ProfileTypes

class ProfileTypeModelTest(TestCase):
    def test_str_returns_name_for_all_profile_types(self):
        for type_enum in ProfileTypes:
            name = type_enum.label  # "Administrador de Sistema", etc.
            profile = ProfileType.objects.create(type=type_enum, name=name)
            self.assertEqual(str(profile), name)