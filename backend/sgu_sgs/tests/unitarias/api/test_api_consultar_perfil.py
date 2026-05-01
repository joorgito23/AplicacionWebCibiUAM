from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Administrador, UsuarioSistema, Tarifa, Contrato
from dateutil.relativedelta import relativedelta
from django.utils import timezone
URL = '/cibiuam/consultar_perfil/'


class ConsultarPerfilAPITest(TransactionTestCase):
    """Prueba la consulta del perfil del usuario"""
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
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=self.user, tarifa=self.tarifa)

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

    def test_000_consultar_perfil(self):
        """Consulta el perfil correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        data = response.data

        # Comprueba que devuelve todos los datos del usuario correctamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["usuario"], "usuario")
        self.assertEqual(data["nombre"], "Prueba")
        self.assertEqual(data["apellidos"], "Prueba")
        self.assertEqual(data["rol"], "usuario")
        self.assertEqual(data["duracion"], "Mensual")
        self.assertEqual(
            data["fin"], timezone.localtime().date()+relativedelta(days=29))
        self.assertEqual(data["saldo"], 0.0)
        self.assertEqual(data["tlf"], "111111111")

    def test_001_consultar_perfil(self):
        """Error en la consulta del perfil al no ser un usuario """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición sin ser usuario
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un usuario.")

    def test_002_consultar_perfil(self):
        """Error en la consulta del perfil al no haberse identificado """

        # Realiza la petición sin estar identificado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
