from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Tarifa
URL = '/cibiuam/informacion/tarifas/'


class ConsultarListaTarifasAPITest(TransactionTestCase):
    """Prueba la obtención de tarifas"""
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

    def test_000_obtener_tarifas(self):
        """Consulta la lista de tarifas correctamente """

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que devuelve el nombre de las tarifas existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get("duracion"), "mensual")
        self.assertEqual(response.data[1].get("duracion"), "semestral")
        self.assertEqual(response.data[2].get("duracion"), "anual")
