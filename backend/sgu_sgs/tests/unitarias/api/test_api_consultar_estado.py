from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Estacion, Anclaje, Bicicleta
URL = '/cibiuam/consultar_estado/'


class ConsultarEstadoAPITest(TransactionTestCase):
    """Prueba la consulta del estado del campus"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.est, numAnclaje=2)
        self.bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)

    def test_000_consultar_estado(self):
        """Consultar estado correctamente """
        data = {'estacion': "Prueba"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post(URL, data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 1)
        self.assertEqual(response.data.get("ocupado"), 1)

    def test_001_consultar_estado(self):
        """Consultar estado de forma errónea al no indicar estación """
        data = {'error': "error"
                }

        # Realiza la petición sin indicar estación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar la estacion.")

    def test_002_consultar_estado(self):
        """Consultar estado de forma errónea al indicar una estación no existente"""
        data = {'estacion': "error"
                }

        # Realiza la petición con una estación no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Estacion no encontrada.")
