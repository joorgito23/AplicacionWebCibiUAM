from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Estacion
URL = '/cibiuam/informacion/estaciones/'


class ConsultarListaEstacionesAPITest(TransactionTestCase):
    """Prueba la obtención de estaciones"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.e = Estacion.objects.create(
            nombre="Prueba", ubicacion="Calle Madrid", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.e.crearAnclajes()
        self.e1 = Estacion.objects.create(
            nombre="Prueba1", ubicacion="Calle Sevilla", latitud=0,
            longitud=0.5, nAnclajes=3)
        self.e1.crearAnclajes()

    def test_000_consultar_estaciones(self):
        """Consulta las estaciones correctamente """

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que devuelve todas las estaciones con su nombre y ubicación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("nombre"), "Prueba")
        self.assertEqual(response.data[1].get("nombre"), "Prueba1")
        self.assertEqual(response.data[0].get("ubicacion"), "Calle Madrid")
        self.assertEqual(response.data[1].get("ubicacion"), "Calle Sevilla")
        self.assertEqual(response.data[0].get(
            "latitud"), "0.00000000000000000")
        self.assertEqual(response.data[0].get(
            "longitud"), "0.50000000000000000")
