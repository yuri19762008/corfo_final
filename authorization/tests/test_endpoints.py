from rest_framework.test import APITestCase
from django.urls import reverse
from authorization.models import ProfileType
from authorization.tests.factories import ProfileTypeFactory
from authentication.tests.factories import user_admin_sistema

class ProfileTypeEndpointTestCase(APITestCase):
    def setUp(self):
        self.admin_user = user_admin_sistema()
        self.client.force_authenticate(user=self.admin_user)  # 👈 loguear como admin
    
    def test_create_profile_type(self):
        data = {
            "type": "nuevo_tipo",
            "name": "Nuevo Tipo"
        }
        response = self.client.post("/api/authorization/profile_types/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ProfileType.objects.filter(type="nuevo_tipo").exists())
    
    def test_update_profile_type(self):
        profile = ProfileTypeFactory(type="original", name="Original")
        data = {"name": "Modificado"}
        url = f"/api/authorization/profile_types/{profile.id}/"
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertEqual(profile.name, "Modificado")

    def test_admin_can_delete_unused_profile_type(self):
        self.client.force_authenticate(user=user_admin_sistema())
        profile_type = ProfileType.objects.create(type="temporal", name="Perfil Temporal")
        response = self.client.delete(f"/api/authorization/profile_types/{profile_type.id}/")
        self.assertEqual(response.status_code, 204)  # No Content

    def test_list_profile_types(self):
        ProfileTypeFactory.create_batch(4)  # 👈 más claro: espera 3
        response = self.client.get("/api/authorization/profile_types/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)