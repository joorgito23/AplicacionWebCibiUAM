from django.test import TransactionTestCase
from sgu_sgs.models import Tarifa
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class TarifaTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")

    def test_001_tarifa_str(self):
        """
        Prueba método str
        """
        self.assertEqual(str(
            self.tarifa), "Duración de la tarifa: mensual. Importe: 10 - Precio por minuto: 0")

    def test_002_tarifa_getDuracion(self):
        """
        Prueba método getDuracion
        """
        # Comprueba que el método devuelve la duración correcta
        self.assertEqual(self.tarifa.getDuracion(), "mensual")

    def test_003_tarifa_obtenerImporte(self):
        """
        Prueba método obtenerImporte
        """
        # Comprueba que el método devuelve el importe de la tarifa
        self.assertEqual(self.tarifa.obtenerImporte(), 10)

    def test_004_tarifa_actualizarImporte(self):
        """
        Prueba método actualizarImporte
        """
        # Comprueba que el método actualiza el importe de la tarifa de forma correcta

        # Actualización incorrecta
        self.assertEqual(self.tarifa.actualizarImporte(-2), False)

        # Actualización correcta
        self.assertEqual(self.tarifa.actualizarImporte(2), True)
        self.assertEqual(Tarifa.objects.all().first().obtenerImporte(), 2)

    def test_005_tarifa_actualizarPrecioMinuto(self):
        """
        Prueba método actualizarPrecioMinuto
        """
        # Comprueba que la tarifa mensual no actualiza el precio por minuto
        self.assertEqual(self.tarifa.actualizarPrecioMinuto(-2), False)
        self.assertEqual(self.tarifa.actualizarPrecioMinuto(2), False)
        # Actualizo precio por minuto de otra tarifa
        t2 = Tarifa.objects.create(
            importe=8, precioMinuto=1, descripcion="Prueba", duracion="anual")
        self.assertEqual(t2.actualizarPrecioMinuto(2), True)
        t = Tarifa.objects.filter(duracion="anual").first()
        self.assertEqual(t.precioMinuto, 2)

    def test_006_tarifa_calcularFechaFin(self):
        """
        Prueba método calcularFechaFin
        """

        # Creacion tarifas de prueba para calcular fecha fin
        tarifa2 = Tarifa.objects.create(
            importe=5, precioMinuto=0.01, descripcion="Prueba2", duracion="semestral")
        tarifa3 = Tarifa.objects.create(
            importe=8, precioMinuto=0.01, descripcion="Prueba3", duracion="anual")

        # Comprueba que la función calcula correctamente la fecha fin del contrato con una tarifa concreta
        self.assertEqual(self.tarifa.calcularFechaFin(
            timezone.localtime().date()), timezone.localtime().date() + relativedelta(days=29))
        self.assertEqual(tarifa2.calcularFechaFin(
            timezone.localtime().date()), timezone.localtime().date() + relativedelta(days=6*30-1))
        self.assertEqual(tarifa3.calcularFechaFin(
            timezone.localtime().date()), timezone.localtime().date() + relativedelta(days=12*30-1))

    def test_007_tarifa_calcularPrecioReservaTarifa(self):
        """
        Prueba método calcularPrecioReservaTarifa
        """
        tarifa2 = Tarifa.objects.create(
            importe=5, precioMinuto=0.01, descripcion="Prueba2", duracion="semestral")
        tarifa3 = Tarifa.objects.create(
            importe=8, precioMinuto=0.01, descripcion="Prueba3", duracion="anual")

        # Comprueba que la función calcula correctamente el precio de una reserva dadas las fechas de inicio y fin
        self.assertEqual(self.tarifa.calcularPrecioReservaTarifa(
            timezone.localtime(), timezone.localtime()-relativedelta(minutes=10)), -1)
        self.assertEqual(self.tarifa.calcularPrecioReservaTarifa(
            timezone.localtime(), timezone.localtime()+relativedelta(minutes=10)), 0)
        self.assertEqual(tarifa2.calcularPrecioReservaTarifa(
            timezone.localtime(), timezone.localtime()+relativedelta(minutes=10)), 0.1)
        self.assertEqual(tarifa3.calcularPrecioReservaTarifa(
            timezone.localtime(), timezone.localtime()+relativedelta(minutes=10)), 0.1)
