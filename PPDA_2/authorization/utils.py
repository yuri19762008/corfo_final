from django.contrib.auth.models import Group, Permission
from rest_framework import permissions
from authorization.models import ProfileTypes

# Diccionario maestro de permisos según perfil
PERMISSIONS_BY_PROFILE_TYPE = {
    ProfileTypes.ADMINISTRADOR_SISTEMA: '__all__',

    ProfileTypes.ADMINISTRADOR_SMA: [
        'add_organismo', 'change_organismo', 'delete_organismo', 'view_organismo',
        'add_tipomedida', 'change_tipomedida', 'delete_tipomedida', 'view_tipomedida',
        'add_medida', 'change_medida', 'delete_medida', 'view_medida',
        'add_plandescontaminacion', 'change_plandescontaminacion', 'delete_plandescontaminacion', 'view_plandescontaminacion',
        'view_reporte',
        'view_profiletype', 
    ],

    ProfileTypes.ANALISTA_SMA: [
        'view_organismo', 'view_tipomedida', 'view_medida', 'view_plandescontaminacion', 'view_reporte',
        'add_medida', 'change_medida', 'delete_medida',
    ],

    ProfileTypes.FUNCIONARIO_SECTORIAL: [
        'view_organismo', 'view_tipomedida', 'view_medida', 'view_plandescontaminacion', 'view_reporte',
        'add_reporte', 'change_reporte',
    ],
}

def setup_groups():
    """Crea o actualiza los grupos y sus permisos según ProfileTypes."""
    for profile_type, permission_list in PERMISSIONS_BY_PROFILE_TYPE.items():
        group, _ = Group.objects.get_or_create(name=profile_type)
        group.permissions.clear()

        if permission_list == '__all__':
            permissions_qs = Permission.objects.all()
        else:
            permissions_qs = Permission.objects.filter(codename__in=permission_list)

        group.permissions.set(permissions_qs)

def apply_permissions_based_on_profile(user):
    """
    Asigna `is_staff`, `is_superuser`, y su grupo con permisos según profile_type.
    """
    tipo = user.profile_type.type

    # Flags especiales
    if tipo == ProfileTypes.ADMINISTRADOR_SISTEMA:
        user.is_staff = True
        user.is_superuser = True
    elif tipo == ProfileTypes.ADMINISTRADOR_SMA:
        user.is_staff = True
        user.is_superuser = False
    else:
        user.is_staff = False
        user.is_superuser = False

    # Asegurar grupos y asignar al usuario
    setup_groups()
    try:
        group = Group.objects.get(name=tipo)
        user.groups.set([group])
    except Group.DoesNotExist:
        user.groups.clear()

def get_permissions_for_profile_type(profile_type):
    """
    Retorna el queryset de permisos esperados según el tipo de perfil.
    """
    if profile_type not in PERMISSIONS_BY_PROFILE_TYPE:
        raise ValueError(f"Perfil no reconocido: {profile_type}")

    if PERMISSIONS_BY_PROFILE_TYPE[profile_type] == '__all__':
        return Permission.objects.all()

    return Permission.objects.filter(codename__in=PERMISSIONS_BY_PROFILE_TYPE[profile_type])