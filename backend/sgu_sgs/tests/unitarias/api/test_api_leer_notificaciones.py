from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Administrador, UsuarioSistema, Tarifa, Contrato
from dateutil.relativedelta import relativedelta
from django.utils import timezone
URL = '/cibiuam/leer_notificaciones/'


class LeerNotificacionesAPITest(TransactionTestCase):
    """Prueba la lectura de notificaciones del usuario"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=self.user, tarifa=self.tarifa)

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

    def test_000_leer_notificaciones(self):
        """Lectura de notificaciones correcta """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Realiza la petición correctamente
        response = self.client.get(URL)
        data = response.data

        # Comprueba que recibe todas las notificaciones no leídas del usuario
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fecha"], str(timezone.localtime().date(
        )-relativedelta(days=25)+relativedelta(days=29)-relativedelta(days=10)))
        self.assertEqual(
            data[0]["msg"], "Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.")

        # Comprueba que no recibe ninguna notificación tras haber leído todas previamente
        response = self.client.get(URL)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)

    def test_001_leer_notificaciones(self):
        """Error en la lectura de notificaciones al no estar identificado """
        # Realiza la petición sin estar identificado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_leer_notificaciones(self):
        """Error en la lectura de notificaciones al no ser usuario """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición sin ser usuario
        response = self.client.get(URL)
        data = response.data

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data["Mensaje"], "Debes ser un usuario.")
