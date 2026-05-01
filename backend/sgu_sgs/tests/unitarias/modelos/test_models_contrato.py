from django.test import TransactionTestCase
from sgu_sgs.models import Contrato, Tarifa, Usuario, UsuarioSistema
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class ContratoTest(TransactionTestCase):
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

    def test_001_contrato_str(self):
        """
        Prueba método str
        """
        self.assertEqual(str(
            self.c), f"Inicio: {timezone.localtime().date()} - Fin: {timezone.localtime().date()+relativedelta(days=29)} - Usuario: usuario - Tarifa: mensual")

    def test_002_contrato_getFin(self):
        """
        Prueba método getFin
        """
        # Verifica que devuelve correctamente el campo fin del contrato
        self.assertEqual(
            self.c.getFin(), timezone.localtime().date()+relativedelta(days=29))
