from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Estacion, Bicicleta, Anclaje, UsuarioSistema, Administrador, Gestor
URL = '/cibiuam/informacion/bicicletas/'


class BicicletasAPITest(TransactionTestCase):
    """Prueba la obtención de bicicletas"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.e = Estacion.objects.create(
            nombre="EPS", ubicacion="TOMAS VALIENTE", latitud=0,
            longitud=0.5, nAnclajes=3)
        self.e.crearAnclajes()
        self.b = Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
            estacion=self.e, numAnclaje=1).first(), estacionInicial=self.e)
        self.b = Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
            estacion=self.e, numAnclaje=2).first(), estacionInicial=self.e)
        self.usuario = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario.set_password("contraadmin")
        self.usuario.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario)

        self.usuario2 = UsuarioSistema(
            username="gestorPrueba",
            rol="gestor")
        self.usuario2.set_password("contragestor")
        self.usuario2.save()
        self.gestorPrueba = Gestor.objects.create(
            usuario=self.usuario2, nombre="luis", apellidos="perez")

    def test_000_consultar_bicicletas(self):
        """Consulta el listado de las bicicletas correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que devuelve el listado de bicicletas correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("id"), 1)
        self.assertEqual(response.data[1].get("id"), 2)

    def test_001_consultar_bicicletas(self):
        """Error en la consulta de bicicletas al no estar identificado """

        # Realiza la petición sin estar identificado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_consultar_bicicletas(self):
        """Error en la consulta de bicicletas al no ser un gestor """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Realiza la petición sin ser gestor
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")
