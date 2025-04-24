"""
Modelos relacionados con la autorización de usuarios y sus tipos de perfil.

Incluye:
- `ProfileTypes`: Enumeración de tipos de perfil predefinidos.
- `ProfileType`: Modelo que representa cada tipo de perfil, vinculado a permisos y grupos.
"""

from django.db import models


class ProfileTypes(models.TextChoices):
    """
    Enumeración de tipos de perfil válidos dentro del sistema.

    Se utiliza como fuente de verdad para los distintos roles que puede tener un usuario.
    Es usada internamente para asociar automáticamente permisos y grupos a cada perfil.
    """
    ADMINISTRADOR_SISTEMA = "administrador_sistema", "Administrador de Sistema"
    FUNCIONARIO_SECTORIAL = "funcionario_sectorial", "Funcionario Sectorial"
    ANALISTA_SMA = "analista_sma", "Analista SMA"
    ADMINISTRADOR_SMA = "administrador_sma", "Administrador SMA"


class ProfileType(models.Model):
    """
    Modelo que representa un tipo de perfil o rol dentro del sistema.
    """

    type = models.CharField(verbose_name="Tipo", max_length=30, unique=True)
    name = models.CharField(verbose_name="Nombre", max_length=30)

    def __str__(self):
        return self.name