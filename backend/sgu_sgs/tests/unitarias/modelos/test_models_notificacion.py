from django.test import TransactionTestCase
from sgu_sgs.models import Notificacion, Usuario, UsuarioSistema
from django.utils import timezone


class NotificacionTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.notificacion = Notificacion.objects.create(
            fecha=timezone.localtime().date(), msg="Prueba", usuario=self.user)

    def test_001_notificacion_str(self):
        """
        Prueba método str
        """
        self.assertEqual(str(self.notificacion),
                         f"{timezone.localtime().date()}: Prueba")

    def test_002_notificacion_notificacionLeida(self):
        """
        Prueba método notificacionLeida
        """
        # Comprueba que el estado inicial de la notificación es correcto
        self.assertEqual(self.notificacion.notificacionLeida(), False)

    def test_003_notificacion_leer(self):
        """
        Prueba método leer
        """

        # Comprueba que al leer una notificación cambia de estado
        self.notificacion.leer()
        self.assertEqual(self.notificacion.leida, True)
        self.assertEqual(Notificacion.objects.all().first().leida, True)
