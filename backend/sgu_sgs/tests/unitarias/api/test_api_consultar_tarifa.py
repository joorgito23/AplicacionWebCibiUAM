from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Tarifa
URL = '/cibiuam/consultar_tarifa/'


class ConsultarTarifaAPITest(TransactionTestCase):
    """Prueba la consulta de tarifas"""
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

    def test_000_consultar_tarifa(self):
        """Consulta la tarifa correctamente """

        data = {'nombre': "semestral"
                }

        # Realiza la petición correctamente
        response = self.client.post(URL, data)

        # Comprueba que los datos devueltos son correctos y coinciden con los de la tarifa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("importe"), 5)
        self.assertEqual(response.data.get("precioMinuto"), 0.01)
        self.assertEqual(response.data.get(
            "descripcion"), "Esta tarifa permite realizar reservas con un coste bajo.")
        self.assertEqual(response.data.get("duracion"), "semestral")

    def test_001_consultar_tarifa(self):
        """Error en la consulta de una tarifa al no indicar una tarifa """

        data = {'error': "error"
                }
        # Realiza la petición sin indicar tarifa
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar la tarifa que desea consultar.")

    def test_002_consultar_tarifa(self):
        """Error en la consulta de una tarifa al indicar una tarifa inexistente"""

        data = {"nombre": "error"
                }

        # Realiza la petición con tarifa no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar una tarifa válida.")
