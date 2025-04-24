# authorization/tests/factories.py
import factory
from authorization.models import ProfileType, ProfileTypes

class ProfileTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfileType
        django_get_or_create = ('type',)

    type = factory.Iterator([
        ProfileTypes.ADMINISTRADOR_SISTEMA,
        ProfileTypes.ADMINISTRADOR_SMA,
        ProfileTypes.ANALISTA_SMA,
        ProfileTypes.FUNCIONARIO_SECTORIAL
    ])
    name = factory.LazyAttribute(lambda obj: obj.type.replace("_", " ").title())