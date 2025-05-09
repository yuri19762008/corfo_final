# Generated by Django 5.2 on 2025-04-24 10:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organismo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255, unique=True)),
                ("descripcion", models.TextField(blank=True, null=True)),
                ("contacto", models.EmailField(blank=True, max_length=254, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TipoMedida",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255, unique=True)),
                ("descripcion", models.TextField(blank=True, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Medida",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255)),
                ("indicador", models.CharField(max_length=255)),
                ("formula_calculo", models.TextField()),
                (
                    "frecuencia_reporte",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("medio_verificacion", models.TextField()),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("pendiente", "Pendiente"),
                            ("en_progreso", "En Progreso"),
                            ("completado", "Completado"),
                        ],
                        default="pendiente",
                        max_length=50,
                    ),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
                (
                    "organismo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.organismo",
                    ),
                ),
                (
                    "tipo_medida",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.tipomedida",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlanDescontaminacion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255, unique=True)),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("arica_parinacota", "Arica y Parinacota"),
                            ("tarapaca", "Tarapacá"),
                            ("antofagasta", "Antofagasta"),
                            ("atacama", "Atacama"),
                            ("coquimbo", "Coquimbo"),
                            ("valparaiso", "Región de Valparaíso"),
                            ("metropolitana", "Metropolitana"),
                            ("ohiggins", "Libertador General Bernardo O'Higgins"),
                            ("maule", "Maule"),
                            ("nuble", "Ñuble"),
                            ("biobio", "Biobío"),
                            ("la_araucania", "La Araucanía"),
                            ("los_rios", "Los Ríos"),
                            ("los_lagos", "Los Lagos"),
                            ("aysen", "Aysén del General Carlos Ibáñez del Campo"),
                            (
                                "magallanes_y_antartica_chilena",
                                "Magallanes y Antártica Chilena",
                            ),
                        ],
                        max_length=255,
                    ),
                ),
                ("descripcion", models.TextField(blank=True, null=True)),
                ("fecha_inicio", models.DateField()),
                ("fecha_fin", models.DateField(blank=True, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
                (
                    "medidas",
                    models.ManyToManyField(
                        blank=True, related_name="planes", to="core.medida"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reporte",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=255)),
                (
                    "medio_verificacion_archivo",
                    models.FileField(
                        blank=True, null=True, upload_to="medios_verificacion/"
                    ),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
                (
                    "creador",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "medida",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reportes",
                        to="core.medida",
                    ),
                ),
            ],
        ),
    ]
