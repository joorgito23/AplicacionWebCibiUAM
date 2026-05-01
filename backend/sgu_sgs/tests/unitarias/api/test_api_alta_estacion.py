from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema, Estacion, Anclaje
URL = '/cibiuam/alta_estacion/'


class AltaEstacionAPITest(TransactionTestCase):
    """Prueba la creación de una estación"""
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

    def test_000_alta_estacion(self):
        """Crea una estación correctamente """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": 0,
                "longitud": 0.5

                }
        # Realiza petición con datos correctos
        response = self.client.post(URL, data)

        # Comprueba que se haya creado la estación y los anclajes de la estación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Estacion.objects.filter(
            nombre="ciencias").first().ubicacion, "Calle Madrid")
        self.assertEqual(Estacion.objects.filter(
            nombre="ciencias").exists(), True)
        self.assertEqual(response.data.get("Mensaje"),
                         "Estación ciencias creada con éxito.")
        self.assertEqual(Estacion.objects.filter(
            nombre="ciencias").first().anclajes.all().count(), 2)
        self.assertEqual(Anclaje.objects.filter(
            estacion=Estacion.objects.filter(nombre="ciencias").first()).count(), 2)
        self.assertEqual(Anclaje.objects.filter(estacion=Estacion.objects.filter(
            nombre="ciencias").first(), numAnclaje=1).exists(), True)
        self.assertEqual(Anclaje.objects.filter(estacion=Estacion.objects.filter(
            nombre="ciencias").first(), numAnclaje=2).exists(), True)

    def test_001_alta_estacion(self):
        """Error en la creación de una estación al no estar identificado """
        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición sin identificación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_alta_estacion(self):
        """Error en la creación de una estación al no ser un gestor """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición correcta sin ser gestor
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")

    def test_003_alta_estacion(self):
        """Error en la creación de una estación al no introducir todos los datos necesarios """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {
            "ubicacion": "Calle Madrid",
            "nAnclajes": 2,
            "latitud": 0,
            "longitud": 0.5
        }

        # Realiza petición sin nombre de estación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

        data = {'nombre': "ciencias",
                "nAnclajes": 2,
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición sin ubicación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición sin número de anclajes
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "longitud": 0.5
                }

        # Realiza petición sin latitud
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

        data = {'nombre': "ciencias",
                "ubicacion": "Calle Madrid",
                "latitud": 0,
                "nAnclajes": 2,
                }

        # Realiza petición sin longitud
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

    def test_004_alta_estacion(self):
        """Error en la creación de una estación al indicar un nombre ya existente """

        # Crea una estación
        Estacion.objects.create(
            nombre="Prueba", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición con nombre ya existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Nombre de la estación ya existente.")

    def test_005_alta_estacion(self):
        """Error en la creación de una estación al introducir un número de anclajes erróneo """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": "error",
                "latitud": 0,
                "longitud": 0.5
                }
        # Realiza petición con número de anclajes que no es un número
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Número de anclajes erróneo.")

        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": -2,
                "latitud": 0,
                "longitud": 0.5
                }

        # Realiza petición con número negativo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Número de anclajes erróneo.")

    def test_006_alta_estacion(self):
        """Error en la creación de una estación al introducir coordenadas erróneas """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": "error",
                "longitud": 0.5
                }
        # Realiza petición con latitud que no es un número
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Coordenadas erróneas.")

        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "latitud": -200,
                "longitud": 0.5
                }

        # Realiza petición con número fuera del rango correcto
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Coordenadas no existentes.")

        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "longitud": "error",
                "latitud": 0.5
                }
        # Realiza petición con latitud que no es un número
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Coordenadas erróneas.")

        data = {'nombre': "Prueba",
                "ubicacion": "Calle Madrid",
                "nAnclajes": 2,
                "longitud": -200,
                "latitud": 0.5
                }

        # Realiza petición con número fuera del rango correcto
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Coordenadas no existentes.")
