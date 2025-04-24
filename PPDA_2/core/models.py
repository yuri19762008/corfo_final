from django.core.exceptions import ValidationError
from django.db import models
from authentication.models import User

#registro de medidas, generación de informes, visualización consolidada, envío de alertas y gestión de permisos
#configuración inicial del sistema: creación de planes, tipos de medida, regiones (fixtures)
#Faltan modelos que representen la lógica de generación de informes anuales consolidados, incluyendo indicadores clave y exportación.
#No se observan validaciones o restricciones adicionales en los modelos (por ejemplo, unicidad de combinaciones, longitud mínima).

class Organismo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    contacto = models.EmailField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class PlanDescontaminacion(models.Model):
    REGION_CHOICES = [
        ('arica_parinacota', 'Arica y Parinacota'),
        ('tarapaca', 'Tarapacá'),
        ('antofagasta', 'Antofagasta'),
        ('atacama', 'Atacama'),
        ('coquimbo', 'Coquimbo'),
        ('valparaiso', 'Región de Valparaíso'),
        ('metropolitana', 'Metropolitana'),
        ('ohiggins', 'Libertador General Bernardo O\'Higgins'),
        ('maule', 'Maule'),
        ('nuble', 'Ñuble'),
        ('biobio', 'Biobío'),
        ('la_araucania', 'La Araucanía'),
        ('los_rios', 'Los Ríos'),
        ('los_lagos', 'Los Lagos'),
        ('aysen', 'Aysén del General Carlos Ibáñez del Campo'),
        ('magallanes_y_antartica_chilena', 'Magallanes y Antártica Chilena'),
    ]

    nombre = models.CharField(max_length=255, unique=True)
    region = models.CharField(max_length=255, choices=REGION_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField() # soporta directamente el formato ISO 8601 -> YYYY-MM-DD
    fecha_fin = models.DateField(blank=True, null=True)
    medidas = models.ManyToManyField('core.Medida', blank=True, related_name='planes') #[1,2,4]

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    # Validacion de fechas
    def clean(self):
        if self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
        
    # Modifica el metodo save para que se active clean automaticamente al guardar un PlanDescontaminacion
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TipoMedida(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

# SMA - Mediante analista SMA publica una medida
class Medida(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]
    organismo = models.ForeignKey(Organismo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_medida = models.ForeignKey(TipoMedida, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=False)
    indicador = models.CharField(max_length=255)
    formula_calculo = models.TextField()
    frecuencia_reporte = models.CharField(max_length=50, blank=True, null=True)
    medio_verificacion = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


# Organismo Sectoral - Mediante el funcinario sectorial publica un reporte a la SMA.
# SMA - Mediante analista SMA puede ver el reporte.
class Reporte(models.Model): 
    medida = models.ForeignKey("core.Medida", on_delete=models.CASCADE, related_name='reportes')
    titulo = models.CharField(max_length=255)
    creador = models.ForeignKey("authentication.User", on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    medio_verificacion_archivo = models.FileField(upload_to='medios_verificacion/', blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.fecha_creacion}"



