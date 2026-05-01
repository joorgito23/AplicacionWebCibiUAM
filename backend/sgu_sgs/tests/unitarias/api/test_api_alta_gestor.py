from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema
URL = '/cibiuam/alta_gestor/'


class AltaGestorAPITest(TransactionTestCase):
    """Prueba la creación de un gestor"""
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

    def test_000_crear_gestor(self):
        """Crea un nuevo gestor """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "gestor",
                'nombre': "gestor",
                'apellidos': "Perez ",
                'contraseña': "contragestor"
                }

        # Realiza la petición con datos correctos
        response = self.client.post(URL, data)

        # Verifica que el sistema haya creado al gestor
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuarioSistema = UsuarioSistema.objects.filter(
            username="gestor").first()
        self.assertEqual(Gestor.objects.filter(
            usuario=usuarioSistema).first().nombre, "gestor")
        self.assertEqual(response.data.get("Mensaje"),
                         "Gestor gestor creado con éxito.")

    def test_001_crear_gestor(self):
        """Error en la creación de un nuevo gestor al no ser un administrador el usuario que intenta crearlo """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'usuario': "gestor2",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contragestor"
                }

        # Realiza la petición sin ser administrador
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un administrador.")

    def test_002_crear_gestor(self):
        """Error en la creación de un nuevo gestor al no indicar todos los datos necesarios """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {
            'nombre': "Pepe",
            'apellidos': "Perez Rodriguez",
            'contraseña': "gestor"
        }

        # Realiza la petición sin usuario
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe completar todos los campos necesarios.")

        data = {'usuario': "gestor2",
                'apellidos': "Perez Rodriguez",
                'contraseña': "gestor"
                }

        # Realiza la petición sin nombre
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe completar todos los campos necesarios.")

        data = {'usuario': "gestor2",
                'nombre': "Pepe",
                'contraseña': "gestor"
                }

        # Realiza la petición sin apellidos
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe completar todos los campos necesarios.")

        data = {'usuario': "gestor2",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez"
                }

        # Realiza petición sin contraseña
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe completar todos los campos necesarios.")

    def test_003_crear_gestor(self):
        """Error en la creación de un nuevo gestor al indicar un usuario ya existente """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "gestorPrueba",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "gestorprueba"
                }

        # Realiza la petición con usuario ya existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(
            "Mensaje"), "Error al crear el gestor. Nombre de usuario ya existente")

    def test_004_crear_gestor(self):
        """Error en la creación de un nuevo gestor al establecer una contraseña demasiado corta """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "gestor2",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "gestor"
                }

        # Realiza la petición con una contraseña poco segura
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Error al crear el gestor. Contraseña poco segura")

    def test_005_crear_gestor(self):
        """Error en la creación de un nuevo gestor al no haberse identificado el administrador"""

        data = {'usuario': "gestor",
                'nombre': "gestor",
                'apellidos': "Perez ",
                'contraseña': "contragestor"
                }

        # Realiza la petición sin identificación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
