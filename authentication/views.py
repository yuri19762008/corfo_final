from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import logging
logger = logging.getLogger(__name__)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

#TODO: Revisar la respuesta de los status de todos las vistas para asegurar manejo de http
class RegisterAPIView(APIView):
    permission_classes = [IsAdminUser] #Obligar a que sólo los administradores puedan crear usuarios

    def post(self, request):
        logger.debug("Estamos en el post de RegisterAPIView")
        register_serializer = UserSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()
        return Response(register_serializer.data, status=status.HTTP_201_CREATED)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Cierre de Sesión Exitoso!."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Error al Cerrar Sesión."}, status=status.HTTP_400_BAD_REQUEST)