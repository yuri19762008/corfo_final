from django.test import TestCase
from core.models import PlanDescontaminacion, Organismo, TipoMedida, Medida, Reporte
from datetime import date

class MedidaModelTest(TestCase):
    """
    Test del modelo Medida.
    
    Verifica:
    - Relaciones entre modelos
    - Método __str__ 
    - Creación de objetos
    - Actualización del campo 'estado'
    - on_delete=models.SET_NULL    
    """

    def setUp(self):
        """
        Crea las instancias necesarias para las pruebas:
        - TipoMedida.
        - Organismo.
        """
        self.tipo = TipoMedida.objects.create(nombre="Regulación")
        self.tipo_update = TipoMedida.objects.create(nombre="Fiscalización")
        self.organismo = Organismo.objects.create(nombre="CONAF")

    def test_crear_medida(self):
        """
        Testea:
        1) Correcta creación del objeto Medida
        2) Método __str__ del modelo Medida retorne el formato esperado.
        El formato esperado es: "<nombre de la medida> - <estado>".
        Por defecto, el estado debería ser 'pendiente' si no se especifica otro.
        """
        medida = Medida.objects.create(
            nombre="Control de emisiones",
            tipo_medida=self.tipo,
            organismo=self.organismo,
            indicador="CO2 < 500ppm",
            formula_calculo="Promedio anual",
            medio_verificacion="Informe técnico"
        )

        # Test 1
        self.assertEqual(medida.nombre, "Control de emisiones")
        self.assertEqual(medida.tipo_medida.nombre, "Regulación")
        self.assertEqual(medida.organismo.nombre, "CONAF")

        # Test 2
        self.assertEqual(str(medida), "Control de emisiones - pendiente")


    def test_actualizar_estado(self):
        """
        Verifica que se pueda actualizar el campo 'estado' a todos los valores válidos.
        Pasar de estado default "pendiente" a 'en_progeso', 'completado' y volver a 'pendiente'
        """
        medida = Medida.objects.create(
            nombre="Reducción de partículas",
            tipo_medida=self.tipo,
            organismo=self.organismo,
            indicador="PM2.5 < 25µg/m3",
            formula_calculo="Promedio anual",
            medio_verificacion="Informe anual"
        )

        estados = ['en_progreso', 'completado', 'pendiente']

        for estado in estados:
            medida.estado = estado
            medida.save()
            self.assertEqual(medida.estado, estado)

    def test_eliminar_tipo_medida(self):
        """
        Verifica que medida.tipo quede NULL si se borra el TipoMedida asociado (on_delete=models.SET_NULL)
        y que se pueda asignar un nuevo TipoMedida
        """
        medida = Medida.objects.create(
            nombre="Control emisiones",
            tipo_medida=self.tipo,
            organismo=self.organismo,
            indicador="CO2 < 500ppm",
            formula_calculo="Promedio anual",
            medio_verificacion="Informe técnico"
        )
        self.tipo.delete()
        medida.refresh_from_db()
        print(medida.tipo_medida)
        self.assertIsNone(medida.tipo_medida)

        medida.tipo_medida = self.tipo_update
        medida.save()
        medida.refresh_from_db()
        self.assertEqual(medida.tipo_medida.nombre, "Fiscalización")


class PlanDescontaminacionModelTest(TestCase):
    """
    Test para el modelo PlanDescontaminacion.
    """

    def test_creacion_plan(self):
        """
        Verifica la correcta creación del objeto PlanDescontaminacion,
        asegurando que los campos requeridos se guarden correctamente.
        """
        plan = PlanDescontaminacion.objects.create(
            nombre="Plan Comuna X",
            descripcion="Plan de control de emisiones en la zona de la Comuna X",
            region="valparaiso",
            fecha_inicio=date(2024, 1, 1)
        )

        self.assertEqual(plan.nombre, "Plan Comuna X")
        self.assertEqual(str(plan), "Plan Comuna X")
        self.assertEqual(plan.region, "valparaiso")
        self.assertEqual(plan.fecha_inicio, date(2024, 1, 1))

