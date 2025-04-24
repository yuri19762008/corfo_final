# authorization/views.py
from rest_framework.viewsets import ModelViewSet
from authorization.models import ProfileType
from authorization.serializers import ProfileTypeSerializer
from authorization.permissions import HasProfileAccess

class ProfileTypeModelViewSet(ModelViewSet):
    queryset = ProfileType.objects.all()
    serializer_class = ProfileTypeSerializer
    permission_classes = [HasProfileAccess]