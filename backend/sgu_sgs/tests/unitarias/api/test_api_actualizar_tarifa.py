from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema, Tarifa
URL = '/cibiuam/actualizar_tarifa/'


class ActualizarTarifaAPITest(TransactionTestCase):
    """Prueba la actualización de tarifas"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
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
        self.mensual = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")
        coste = 0.01
        self.semestral = Tarifa.objects.create(
            importe=5, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")
        self.anual = Tarifa.objects.create(
            importe=8, precioMinuto=coste, descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

    def test_000_actualizar_tarifa(self):
        """Actualiza la tarifa correctamente """

        # Actualiza precio por minuto e importe

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": 2
                }
        # Realiza la petición con datos correctos
        response = self.client.post(URL, data)

        # Verifica que la tarifa tenga el nuevo precio por minuto e importe
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tarifa.objects.filter(
            duracion="semestral").first().importe, 2)
        self.assertEqual(Tarifa.objects.filter(
            duracion="semestral").first().importe, 2)
        self.assertEqual(response.data.get("Mensaje"),
                         "Tarifa actualizada con éxito.")

    def test_001_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al no estar identificado """
        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": 2
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verifica código de respuesta esperado
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al no ser un gestor """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": 2
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")

    def test_003_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al no introducir todos los datos necesarios """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {
            "importe": 2,
            "precioMinuto": 2
        }

        # Realiza la petición sin tarifa
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(
            "Mensaje"), "Debe indicar tarifa y nuevo importe o precio por minuto.")

        data = {'nombre': "semestral",
                }

        # Realiza la petición sin importe ni precio por minuto
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(
            "Mensaje"), "Debe indicar tarifa y nuevo importe o precio por minuto.")

    def test_004_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al introducir una tarifa no existente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "error",
                "importe": 2,
                "precioMinuto": 2
                }
        # Realiza la petición con tarifa incorrecta
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar una tarifa válida.")

    def test_005_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al introducir un importe erróneo """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "semestral",
                "importe": "error",
                "precioMinuto": 2
                }

        # Realiza la petición con importe erróneo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"), "Importe erróneo.")

        data = {'nombre': "semestral",
                "importe": -5,
                "precioMinuto": 2
                }
        # Realiza la petición con importe negativo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Error al actualizar el importe de la tarifa.")

    def test_006_actualizar_tarifa(self):
        """Actualiza la tarifa de forma errónea al introducir un precio por minuto erróneo o intentar actualizar el precio por minuto de la tarifa mensual"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": "error"
                }

        # Realiza la petición con precio por minuto inválido
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Precio por minuto erróneo.")

        data = {'nombre': "mensual",
                "importe": 2,
                "precioMinuto": 2
                }
        # Realiza la petición para actualizar el precio por minuto de la tarifa mensual
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(
            "Mensaje"), "No se puede actualizar el precio por minuto de la tarifa mensual.")

        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": -2
                }
        # Realiza la petición con precio por minuto negativo
        response = self.client.post(URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(
            "Mensaje"), "Error al actualizar el precio por minuto de la tarifa.")
