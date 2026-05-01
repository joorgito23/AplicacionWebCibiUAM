from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Estacion, Bicicleta, Anclaje, UsuarioSistema, Administrador, Gestor
URL = '/cibiuam/informacion/gestores/'


class GestoresAPITest(TransactionTestCase):
    """Prueba la obtención de gestores"""
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

        self.usuario2 = UsuarioSistema(
            username="gestorPrueba2",
            rol="gestor")
        self.usuario2.set_password("contragestor")
        self.usuario2.save()
        self.gestorPrueba = Gestor.objects.create(
            usuario=self.usuario2, nombre="jesus", apellidos="perez")

    def test_000_consultar_gestores(self):
        """Consulta los gestores correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que devuelve el nombre de usuario de todos los gestores
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get(
            "usuario").get("username"), "gestorPrueba")
        self.assertEqual(response.data[1].get(
            "usuario").get("username"), "gestorPrueba2")

    def test_001_consultar_gestores(self):
        """Error en la consulta de gestores al no estar identificado """

        # Realiza la petición sin estar identificado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_consultar_gestores(self):
        """Error en la consulta de gestores al no ser administrador """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición sin ser administrador
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un administrador.")
