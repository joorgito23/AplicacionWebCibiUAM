from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema


class Intregacion_4_Test(TransactionTestCase):
    """Test de integración 4
        Realiza las acciones cotidianas de un administrador que desea gestionar los gestores del sistema:
        - Realiza login
        - Crea un nuevo gestor contratado
        - Da de baja a otro gestor que ha sido despedido
        - Realiza logout
    """
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

    def test_integracion_4(self):
        # Iniciamos sesión
        data = {'username': "admin",
                "password": "contraadmin"
                }

        # Realiza la petición correctamente con credenciales de un administrador
        response = self.client.post('/auth/token/login', data=data)

        token = response.data.get("auth_token")

        # Crea gestor
        data = {'usuario': "gestor",
                'nombre': "jose",
                'apellidos': "Perez ",
                'contraseña': "contragestor"
                }

        # Realiza la petición con datos correctos
        response = self.client.post(
            '/cibiuam/alta_gestor/', data=data, headers={'Authorization': f'Token {token}'})

        # Verifica que el sistema haya creado al gestor
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuarioSistema = UsuarioSistema.objects.filter(
            username="gestor").first()
        self.assertEqual(Gestor.objects.filter(
            usuario=usuarioSistema).first().nombre, "jose")
        self.assertEqual(response.data.get("Mensaje"),
                         "Gestor gestor creado con éxito.")

        # Obtenemos lista de gestores

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/informacion/gestores/', headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve el nombre de usuario de todos los gestores
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get(
            "usuario").get("username"), "gestorPrueba")
        self.assertEqual(response.data[1].get(
            "usuario").get("username"), "gestor")

        # Baja de un gestor debido a su despido

        data = {'usuario': "gestorPrueba"
                }

        # Realiza la petición con datos correctos
        response = self.client.delete(
            '/cibiuam/baja_gestor/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que el gestor se ha borrado y no existe en el sistema
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UsuarioSistema.objects.filter(
            username="gestorPrueba").exists(), False)
        self.assertEqual(Gestor.objects.filter(nombre="luis").exists(), False)
        self.assertEqual(response.data.get("Mensaje"),
                         "Gestor gestorPrueba borrado con éxito.")
