# authentication/tests/factories.py
import factory
from authentication.models import User
from authorization.models import ProfileType, ProfileTypes
from authorization.tests.factories import ProfileTypeFactory
from authorization.utils import apply_permissions_based_on_profile

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'securepass123')
    first_name = 'Test'
    last_name = 'User'
    profile_type = factory.SubFactory(ProfileTypeFactory)

    is_staff = False
    is_superuser = False


# Helpers para crear usuarios con perfil específico

def user_admin_sistema():
    profile = ProfileTypeFactory(type=ProfileTypes.ADMINISTRADOR_SISTEMA)
    user = UserFactory(profile_type=profile)
    apply_permissions_based_on_profile(user)
    user.save()
    return user

def user_admin_sma():
    profile, _ = ProfileType.objects.get_or_create(type=ProfileTypes.ADMINISTRADOR_SMA)
    user = UserFactory(profile_type=profile)
    apply_permissions_based_on_profile(user)
    user.save()
    return UserFactory(profile_type=profile, is_staff=True, is_superuser=False)

def user_analista_sma():
    profile, _ = ProfileType.objects.get_or_create(type=ProfileTypes.ANALISTA_SMA)
    user = UserFactory(profile_type=profile)
    apply_permissions_based_on_profile(user)
    user.save()
    return UserFactory(profile_type=profile, is_staff=False, is_superuser=False)

def user_funcionario_sectorial():
    profile, _ = ProfileType.objects.get_or_create(type=ProfileTypes.FUNCIONARIO_SECTORIAL)
    user = UserFactory(profile_type=profile)
    apply_permissions_based_on_profile(user)
    user.save()
    return UserFactory(profile_type=profile, is_staff=False, is_superuser=False)