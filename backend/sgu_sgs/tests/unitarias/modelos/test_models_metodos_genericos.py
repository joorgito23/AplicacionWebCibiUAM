from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Usuario, Tarifa, Contrato, Estacion, Anclaje, Bicicleta
from sgu_sgs.models import usuarioExistente, getAnclajeByID, getEstacionByName, getBicicletaByID, getTarifaByName, getUsuarioSistemaByName
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class UsuarioModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=self.user, tarifa=self.tarifa)
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Calle Madrid", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.est.crearAnclajes()
        self.bici = Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
            estacion=self.est, numAnclaje=1).first(), estacionInicial=self.est)

    def test_001_usuarioExistente(self):
        """
        Prueba método usuarioExistente
        """

        # Verifica si la función determina correctamente si un usuario existe o no
        self.assertEqual(usuarioExistente("usuario"), True)
        self.assertEqual(usuarioExistente("user"), False)

    def test_002_getUsuarioSistemaByName(self):
        """
        Prueba método getUsuarioSistemaByName
        """

        # Comprueba que el método obtiene el usuario del sistema a partir del nombre de usuario
        self.assertEqual(getUsuarioSistemaByName("usuario"), self.usuario)
        self.assertEqual(getUsuarioSistemaByName("error"), None)

    def test_003_getTarifaByName(self):
        """
        Prueba método getTarifaByName
        """

        # Verifica que el método obtiene la tarifa a partir de su nombre
        self.assertEqual(getTarifaByName("mensual"), self.tarifa)
        self.assertEqual(getTarifaByName("error"), None)

    def test_004_getEstacionByName(self):
        """
        Prueba método getEstacionByName
        """

        # Verifica que el método obtiene la estación a partir de su nombre
        self.assertEqual(getEstacionByName("Prueba"), self.est)
        self.assertEqual(getEstacionByName("error"), None)

    def test_005_getAnclajeByID(self):
        """
        Prueba método getAnclajeByID
        """

        # Verifica que el método obtiene el anclaje a partir de su ID
        self.assertEqual(getAnclajeByID(
            1), Anclaje.objects.filter(id=1).first())
        self.assertEqual(getAnclajeByID(50), None)

    def test_006_getBicicletaByID(self):
        """
        Prueba método getBicicletaByID
        """

        # Verifica que el método obtiene la bicicleta a partir de su ID
        self.assertEqual(getBicicletaByID(1), self.bici)
        self.assertEqual(getBicicletaByID(4), None)
