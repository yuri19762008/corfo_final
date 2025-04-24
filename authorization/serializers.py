# authorization/serializers.py
from rest_framework import serializers
from .models import ProfileType

class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileType
        fields = ['id', 'type', 'name']