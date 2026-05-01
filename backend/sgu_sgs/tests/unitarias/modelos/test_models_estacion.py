from django.test import TransactionTestCase
from sgu_sgs.models import Estacion, Anclaje, Bicicleta
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class EstacionModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Calle Madrid", latitud=0,
            longitud=0.5, nAnclajes=2)

    def test_001_estacion_str(self):
        """
        Prueba método str
        """
        self.assertEqual(str(self.est), "Prueba - Calle Madrid: 2 anclajes")

    def test_002_estacion_crearAnclajes(self):
        """
        Prueba método crearAnclajes
        """
        # Verifica que se hayan creado los anclajes asociados a la estación
        self.est.crearAnclajes()
        self.assertEqual(Anclaje.objects.filter(estacion=self.est).count(), 2)

    def test_003_estacion_getAnclajeByNumAnclaje(self):
        """
        Prueba método getAnclajeByNumAnclaje
        """
        # Verifica que el método devuelve correctamente el anclaje de una estación a partir de su número
        self.est.crearAnclajes()
        self.assertEqual(self.est.getAnclajeByNumAnclaje(
            1), Anclaje.objects.filter(estacion=self.est, numAnclaje=1).first())

    def test_004_estacion_getDisponibilidadAnclajeBicicleta(self):
        """
        Prueba método getDisponibilidadAnclajeBicicleta
        """
        # Crea anclajes y bicicletas y las asigna a un anclaje de la estación
        self.est.crearAnclajes()
        Bicicleta.objects.create(estacionInicial=self.est, anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=1).first())

        # Comprueba que calcula correctamente la disponibilidad de anclajes y bicicletas
        data = self.est.getDisponibilidadAnclajeBicicleta()
        self.assertEqual(data["libre"], 1)
        self.assertEqual(data["ocupado"], 1)

    def test_005_estacion_seleccionarAnclajeOrigen(self):
        """
        Prueba método seleccionarAnclajeOrigen
        """
        # Crea anclajes
        self.est.crearAnclajes()

        # Comprueba que devuelve None si la estación no tiene ninguna bicicleta
        self.assertEqual(self.est.seleccionarAnclajeOrigen(
            timezone.localtime()+relativedelta(hours=1)), None)

        # Creamos bicicleta y la asigna a un anclaje de la estación
        Bicicleta.objects.create(estacionInicial=self.est, anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=2).first())

        # Comprueba que devuelve correctamente el anclaje de origen recorriendo los anclajes de la estación
        self.assertEqual(self.est.seleccionarAnclajeOrigen(
            timezone.localtime()+relativedelta(hours=1)), self.est.getAnclajeByNumAnclaje(2))

    def test_006_estacion_seleccionarAnclajeDestino(self):
        """
        Prueba método seleccionarAnclajeDestino
        """
        # Crea anclajes
        self.est.crearAnclajes()

        # Comprueba que devuelve el anclaje si la estación tiene un anclaje vacío
        self.assertEqual(self.est.seleccionarAnclajeDestino(
            timezone.localtime()+relativedelta(hours=1)), self.est.getAnclajeByNumAnclaje(1))

        # Creamos bicicleta y la asignamos a un anclaje de la estación
        Bicicleta.objects.create(estacionInicial=self.est, anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=2).first())
        Bicicleta.objects.create(estacionInicial=self.est, anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=1).first())

        # Comprueba que devuelve None puesto que no hay anclajes libres
        self.assertEqual(self.est.seleccionarAnclajeDestino(
            timezone.localtime()+relativedelta(hours=1)), None)
