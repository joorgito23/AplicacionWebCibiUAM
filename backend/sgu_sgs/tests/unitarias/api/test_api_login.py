from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema, Usuario
URL = '/auth/token/login'
URL2 = '/auth/token/logout'


class LoginAPITest(TransactionTestCase):
    """Prueba la autenticación de usuarios"""
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

        self.usuario3 = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario3.set_password("contrausuario")
        self.usuario3.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario3, nombre="jorge", apellidos="perez", tlf="111111111", saldo=0)

    def test_000_login(self):
        """Login correcto """

        data = {'username': "usuario",
                "password": "contrausuario"
                }

        # Realiza la petición correctamente con credenciales de un usuario
        response = self.client.post(URL, data)

        # Comprueba que el login es correcto y devuelve el token y el rol
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("auth_token", response.data)
        self.assertEqual("usuario", response.data.get("rol"))

        data = {'username': "gestorPrueba",
                "password": "contragestor"
                }
        # Realiza la petición correctamente con credenciales de un gestor
        response = self.client.post(URL, data)

        # Comprueba que el login es correcto y devuelve el token y el rol
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("auth_token", response.data)
        self.assertEqual("gestor", response.data.get("rol"))

        data = {'username': "admin",
                "password": "contraadmin"
                }

        # Realiza la petición correctamente con credenciales de un administrador
        response = self.client.post(URL, data)

        # Comprueba que el login es correcto y devuelve el token y el rol
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("auth_token", response.data)
        self.assertEqual("administrador", response.data.get("rol"))

    def test_001_login(self):
        """Login erróneo al introducir credenciales erróneas"""

        data = {'username': "usuario",
                "password": "contrausuar"
                }

        # Realiza la petición con datos inválidos
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Unable to log in with provided credentials.",
                         response.data.get("non_field_errors")[0])

        data = {
            "password": "contragestor"
        }

        # Realiza la petición sin nombre de usuario
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Unable to log in with provided credentials.",
                         response.data.get("non_field_errors")[0])

        # Realiza la petición sin contraseña
        data = {'username': "admin"
                }

        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Unable to log in with provided credentials.",
                         response.data.get("non_field_errors")[0])

    def test_002_logout(self):
        """Logout correcto """

        data = {'username': "usuario",
                "password": "contrausuario"
                }

        # Realiza la petición de login con datos correctos
        response = self.client.post(URL, data)
        # Realiza logout
        response = self.client.post(
            URL2, headers={'Authorization': f'Token {response.data.get("auth_token")}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_003_logout(self):
        """Logout erróneo al no indicar token válido"""

        data = {
        }
        # Realiza petición con token de acceso erróneo
        response = self.client.post(
            URL2, data, headers={'Authorization': 'Token fdbvfsv'})

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
