from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema, Estacion, Anclaje, Bicicleta
URL = '/cibiuam/alta_bicicleta/'


class AltaBicicletaAPITest(TransactionTestCase):
    """Prueba la creación de una bicicleta"""
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
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)

    def test_000_alta_bicicleta(self):
        """Crea una bicicleta correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'estacion': "Prueba",
                "anclajeId": 1
                }
        # Realiza la petición con datos correctos
        response = self.client.post(URL, data)

        # Verifica que la bicicleta se haya creado y la respuesta sea la esperada
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bicicleta.objects.filter(
            estacionInicial=self.est, anclajeInicio=self.anc).exists(), True)
        self.assertEqual(response.data.get("Mensaje"),
                         "Bicicleta creada con éxito.")

    def test_001_alta_bicicleta(self):
        """Error en la creación de una bicicleta al no estar identificado """
        data = {'estacion': "Prueba",
                "anclajeId": 1
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_alta_bicicleta(self):
        """Error en la creación de una bicicleta al no ser un gestor """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'estacion': "Prueba",
                "anclajeId": 1
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")

    def test_003_alta_bicicleta(self):
        """Error en la creación de una bicicleta al no introducir todos los datos necesarios """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'estacion': "Prueba"
                }

        # Realiza la petición sin anclaje id
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

        data = {
            "anclajeId": 1
        }

        # Realiza la petición sin estación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")

    def test_004_alta_bicicleta(self):
        """Error en la creación de una bicicleta al introducir un nombre de estación no existente """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'estacion': "error",
                "anclajeId": 1
                }

        # Realiza la petición con estación no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Estacion no existente.")

    def test_005_alta_bicicleta(self):
        """Error en la creación de una bicicleta al indicar un número de anclaje erróneo """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'estacion': "Prueba",
                "anclajeId": "error"
                }

        # Realiza la petición con número de anclaje inválido
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Número de anclaje erróneo.")

        data = {'estacion': "Prueba",
                "anclajeId": -2
                }
        # Realiza la petición con anclajeId negativo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Número de anclaje erróneo.")

        data = {'estacion': "Prueba",
                "anclajeId": 8
                }

        # Realiza la petición con anclaje no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Anclaje con número 8 no existente.")

    def test_006_alta_bicicleta(self):
        """Error en la creación de una bicicleta al asignarla a un anclaje ya ocupado """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Asigna una bicicleta a un anclaje
        Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        data = {'estacion': "Prueba",
                "anclajeId": 1
                }

        # Realiza la petición con un anclajeId ya ocupado
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Anclaje 1 de la estacion Prueba ocupado.")
