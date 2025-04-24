from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from authorization.utils import apply_permissions_based_on_profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este correo ya está registrado.")]
    )
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'profile_type',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return value

    def create(self, validated_data):
        instance = User(**validated_data)
        instance.set_password(validated_data.get("password"))  # encripta la contraseña
        instance.save()
        apply_permissions_based_on_profile(instance)
        instance.save()
        return instance
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Obtén el token y el refresh token
        user = self.user

        # Agrega información adicional del usuario al token
        data.update({
            "user_id": user.id,
            "email": user.email,  # Puedes agregar otros campos si es necesario
            "full_name": user.get_full_name(),  # Si tienes métodos personalizados en el modelo User
        })

        return data