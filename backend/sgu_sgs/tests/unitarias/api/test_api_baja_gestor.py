from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema
URL = '/cibiuam/baja_gestor/'


class BajaGestorAPITest(TransactionTestCase):
    """Prueba el borrado de un gestor"""
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
            username="gestorBorrado",
            rol="gestor")
        self.usuario3.set_password("contragestor")
        self.usuario3.save()
        Gestor.objects.create(
            usuario=self.usuario3, nombre="jesus", apellidos="rodriguez")

    def test_000_borrar_gestor(self):
        """Borra un gestor correctamente """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "gestorBorrado"
                }

        # Realiza la petición con datos correctos
        response = self.client.delete(URL, data)

        # Comprueba que el gestor se ha borrado y no existe en el sistema
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UsuarioSistema.objects.filter(
            username="gestorBorrado").exists(), False)
        self.assertEqual(Gestor.objects.filter(nombre="jesus").exists(), False)
        self.assertEqual(response.data.get("Mensaje"),
                         "Gestor gestorBorrado borrado con éxito.")

    def test_001_borrar_gestor(self):
        """Error en la eliminación de un gestor al no realizarlo un administrador """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'usuario': "gestorBorrado"
                }

        # Realiza la petición sin ser administrador
        response = self.client.delete(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un administrador.")

    def test_002_borrar_gestor(self):
        """Error en la eliminación de un gestor al no indicar nombre de usuario """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'error': "error"
                }
        # Realiza la petición sin indicar nombre de usuario
        response = self.client.delete(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar el gestor a borrar.")

    def test_003_borrar_gestor(self):
        """Error en la eliminación de un gestor al indicar un usuario que no existe """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "noExiste"
                }

        # Realiza la petición al indicar usuario no existente
        response = self.client.delete(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Error al borrar el gestor. Gestor no existente")

    def test_004_borrar_gestor(self):
        """Error en la eliminación de un gestor al indicar un usuario que no es gestor """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'usuario': "admin"
                }
        # Realiza la petición con un nombre de usuario que no pertenece a un gestor
        response = self.client.delete(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Error al borrar el gestor. Gestor no existente")

    def test_005_borrar_gestor(self):
        """Error en la eliminación de un gestor al no haberse identificado el administrador"""

        data = {'usuario': "gestorBorrado"
                }

        # Realiza la petición sin identificarse
        response = self.client.delete(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
