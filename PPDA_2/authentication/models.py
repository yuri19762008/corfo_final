from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import is_password_usable
from authorization.models import ProfileType,ProfileTypes
from authorization.utils import apply_permissions_based_on_profile

import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, profile_type, password, **extra_fields):
        logging.debug("Estamos en create_user")
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")

        # Acepta ID o instancia de ProfileType
        if not isinstance(profile_type, ProfileType):
            try:
                profile_type = ProfileType.objects.get(id=profile_type)
            except ProfileType.DoesNotExist:
                raise ValueError("El tipo de perfil indicado no existe.")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            profile_type=profile_type, 
            **extra_fields
        )
        user.set_password(password)
        user.save()  # GUARDAR ANTES DE GRUPOS
        apply_permissions_based_on_profile(user)  # ahora sí: se puede usar user.groups.set()
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        logging.debug("Estamos en create_superuser")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        # Asignar tipo de perfil automáticamente
        profile_type = ProfileType.objects.get(type=ProfileTypes.ADMINISTRADOR_SISTEMA)
        return self.create_user(email, first_name, last_name, profile_type, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(verbose_name='Correo Electrónico', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='Nombre', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Apellido', max_length=255, blank=True)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # profile_type se asigna en create_superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Protección contra contraseñas sin hash
        if self.password and is_password_usable(self.password):
            if not self.password.startswith(('pbkdf2_', 'argon2$', 'bcrypt$', 'sha1$')):
                logging.debug("Aplicando hash")
                self.set_password(self.password)
        super().save(*args, **kwargs)