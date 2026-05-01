from django.test import TransactionTestCase
from sgu_sgs.models import Estacion, Anclaje, Bicicleta, Usuario, UsuarioSistema, Tarifa, Contrato
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta


class BicicletaModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Calle Madrid", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.est.crearAnclajes()
        self.est2 = Estacion.objects.create(
            nombre="Prueba2", ubicacion="Calle Sevilla", latitud=2,
            longitud=2.5, nAnclajes=2)
        self.est2.crearAnclajes()
        self.bici = Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=1).first(), estacionInicial=self.est)
        self.usuario = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        self.usuario.set_password("contrausuario1")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=179), usuario=self.user, tarifa=self.tarifa)

    def test_001_bicicleta_str_(self):
        """
        Prueba método str
        """
        self.assertEqual(str(
            self.bici), "Bicicleta ubicada inicialmente en el anclaje número 1 de la estación Prueba")

    def test_002_bicicleta_anclajeBicicleta(self):
        """
        Prueba método anclajeBicicleta
        """

        # Prueba el caso en el que no se ha hecho ninguna reserva con la bicicleta. Se encuentra en el momento actual en su anclaje inicial
        # Verifica que devuelva el anclaje en el que se encuentra la bicicleta
        self.assertEqual(self.bici.anclajeBicicleta(), Anclaje.objects.filter(
            estacion=self.est, numAnclaje=1).first())

    def test_003_bicicleta_anclajeBicicleta(self):
        """
        Prueba método anclajeBicicleta
        """
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=100), fechaFin=timezone.localtime()-relativedelta(minutes=85), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.est.getAnclajeByNumAnclaje(1), ancDestino=self.est2.getAnclajeByNumAnclaje(1), bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() - timedelta(minutes=100))

        # Prueba el caso en el que se han hecho reservas previas con la bicicleta. Se encuentra en el momento actual en el anclaje destino de la última reserva
        # Verifica que devuelva el anclaje en el que se encuentra la bicicleta
        self.assertEqual(self.bici.anclajeBicicleta(), Anclaje.objects.filter(
            estacion=self.est2, numAnclaje=1).first())

    def test_004_bicicleta_anclajeBicicleta(self):
        """
        Prueba método anclajeBicicleta
        """
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=20), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.est.getAnclajeByNumAnclaje(1), ancDestino=self.est2.getAnclajeByNumAnclaje(1), bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() - timedelta(minutes=100))

        # Prueba el caso en el que la bicicleta está en uso actualmente
        # Verifica que no devuelva ningún anclaje
        self.assertEqual(self.bici.anclajeBicicleta(), None)
