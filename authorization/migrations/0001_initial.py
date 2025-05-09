# Generated by Django 5.2 on 2025-04-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProfileType",
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
                (
                    "type",
                    models.CharField(max_length=30, unique=True, verbose_name="Tipo"),
                ),
                ("name", models.CharField(max_length=30, verbose_name="Nombre")),
            ],
        ),
    ]
