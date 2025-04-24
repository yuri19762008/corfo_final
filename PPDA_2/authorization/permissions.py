from rest_framework import permissions
from .models import ProfileTypes

def has_profile_permission(user, method):
    """
    Verifica si el usuario tiene permiso para un método HTTP según su perfil.
    - ADMINISTRADOR_SISTEMA: acceso total
    - ADMINISTRADOR_SMA: solo lectura
    - Otros: acceso denegado
    """
    if not user or not user.is_authenticated:
        return False

    tipo = getattr(getattr(user, 'profile_type', None), 'type', None)

    if tipo == ProfileTypes.ADMINISTRADOR_SISTEMA:
        return True
    elif tipo == ProfileTypes.ADMINISTRADOR_SMA:
        return method in permissions.SAFE_METHODS
    return False
class HasProfileAccess(permissions.BasePermission):
    """
    Permiso DRF que delega la lógica de autorización por perfil a `authorization.utils.has_profile_permission`.

    Acceso definido por tipo de perfil:
    - ADMINISTRADOR_SISTEMA: acceso total (GET, POST, PUT, PATCH, DELETE)
    - ADMINISTRADOR_SMA: solo lectura (GET, HEAD, OPTIONS)
    - Otros: acceso denegado
    """

    def has_permission(self, request, view):
        return has_profile_permission(request.user, request.method)