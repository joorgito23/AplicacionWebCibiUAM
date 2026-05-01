from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, UsuarioSistema, Tarifa, Contrato, Gestor
from dateutil.relativedelta import relativedelta
from django.utils import timezone
URL = '/cibiuam/consultar_contratos/'


class ConsultarContratosAPITest(TransactionTestCase):
    """Prueba la consulta de contratos de los usuarios"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.mensual = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")
        coste = 0.01
        self.semestral = Tarifa.objects.create(
            importe=5, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")
        self.anual = Tarifa.objects.create(
            importe=8, precioMinuto=coste, descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

        self.usuario2 = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        self.usuario2.set_password("contrausuario")
        self.usuario2.save()
        self.user2 = Usuario.objects.create(
            usuario=self.usuario2, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(
            days=6*30), fin=timezone.localtime().date()-relativedelta(days=1), usuario=self.user, tarifa=self.semestral)
        self.c1 = Contrato.objects.create(inicio=timezone.localtime().date()+relativedelta(
            days=6*30), fin=timezone.localtime().date()+relativedelta(days=18*30-1), usuario=self.user2, tarifa=self.anual)

        self.usuario3 = UsuarioSistema(
            username="gestor",
            rol="gestor")
        self.usuario3.set_password("contragestor")
        self.usuario3.save()
        self.gestor = Gestor.objects.create(
            usuario=self.usuario3, nombre="Gestor", apellidos="perez")

    def test_000_consultar_contratos(self):
        """Consulta los contratos correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario3)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que los contratos obtenidos son los correctos y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )-relativedelta(days=6*30)), response.data[1].get("inicio"))
        self.assertEqual(
            str(timezone.localtime().date()-relativedelta(days=1)), response.data[1].get("fin"))
        self.assertEqual("semestral", response.data[1].get(
            "tarifa").get("duracion"))

        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )+relativedelta(days=6*30)), response.data[0].get("inicio"))
        self.assertEqual(str(timezone.localtime().date() +
                         relativedelta(days=18*30-1)), response.data[0].get("fin"))
        self.assertEqual("anual", response.data[0].get(
            "tarifa").get("duracion"))

    def test_001_consultar_contratos(self):
        """Error en la consulta de los contratos al no ser un gestor """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición sin ser gestor
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")

    def test_002_consultar_contratos(self):
        """Error en la consulta de los contratos al no estar identificado """

        # Realiza la petición sin estar identificado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
