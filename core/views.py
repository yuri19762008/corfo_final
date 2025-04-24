from rest_framework import viewsets
from django.db.models import Q
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import PlanDescontaminacion, Organismo, TipoMedida, Medida, Reporte
from .serializers import OrganismoSerializer, PlanDescontaminacionSerializer, MedidaSerializer, TipoMedidaSerializer, ReporteSerializer

from authorization.permissions import HasProfileAccess


import logging
logger = logging.getLogger(__name__)

class OrganismoViewSet(viewsets.ModelViewSet):
    queryset = Organismo.objects.all()
    serializer_class = OrganismoSerializer
    permission_classes = [HasProfileAccess]

    @action(detail=True, methods=['get'])
    def medidas_asignadas(self, request, pk=None):
        organismo = self.get_object()
        
        queryset = Medida.objects.filter(organismo=organismo)
        logging.debug(f"Este es el queryset {queryset}")
        medidas = [medida.nombre for medida in queryset]
        return Response({'Organismo': organismo.nombre, 'Medidas': medidas})

class PlanDescontaminacionViewSet(viewsets.ModelViewSet):
    queryset = PlanDescontaminacion.objects.all()
    serializer_class = PlanDescontaminacionSerializer
    permission_classes = [HasProfileAccess]

class MedidaViewSet(viewsets.ModelViewSet):
    queryset = Medida.objects.all()
    serializer_class = MedidaSerializer
    permission_classes = [HasProfileAccess]

    @action(detail=False, methods=['get'])
    def estado_medidas(self, request):
        estado_medidas = {}

        for medida in Medida.objects.all():
            if medida.estado in estado_medidas.keys():
                estado_medidas[medida.estado].append(medida.nombre)
            else:
                estado_medidas[medida.estado] = [medida.nombre]

        return Response(estado_medidas)

class TipoMedidaViewSet(viewsets.ModelViewSet):
    queryset = TipoMedida.objects.all()
    serializer_class = TipoMedidaSerializer
    permission_classes = [HasProfileAccess]

    @action(detail=True, methods=['get'])
    def medidas_tipo(self, request, pk=None):
        tipo = self.get_object()
        queryset = Medida.objects.filter(tipo_medida=tipo).values('tipo_medida__nombre').annotate(total=models.Count('tipo_medida'))
        medidas = [medida for medida in queryset]

        return Response(medidas)

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [HasProfileAccess]

