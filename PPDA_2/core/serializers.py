from rest_framework import serializers
from .models import Organismo, PlanDescontaminacion, Medida, TipoMedida, Reporte

class OrganismoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organismo
        fields = '__all__'


class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'

class PlanDescontaminacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDescontaminacion
        fields = '__all__'

class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
