from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Administrador, UsuarioSistema, Tarifa, Contrato
from dateutil.relativedelta import relativedelta
from django.utils import timezone
URL = '/cibiuam/modificar_perfil/'


class ModificarPerfilAPITest(TransactionTestCase):
    """Prueba la modificación del perfil del usuario"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=self.user, tarifa=self.tarifa)

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

    def test_000_modificar_perfil(self):
        """Modifica el perfil correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'tlf': "222222222"
                }

        # Realiza la petición correctamente
        response = self.client.post(URL, data=data)
        data = response.data

        # Comprueba que se haya actualizado el teléfono
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["Mensaje"], "Datos actualizados correctamente.")
        self.assertEqual(Usuario.objects.filter(
            usuario=self.usuario).first().tlf, "222222222")

    def test_001_modificar_perfil(self):
        """Error en la modificación del perfil al no ser un usuario """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'tlf': "222222222"
                }

        # Realiza la petición sin ser usuario
        response = self.client.post(URL, data=data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un usuario.")

    def test_002_modificar_perfil(self):
        """Error en la modificación del perfil al no pasar número de teléfono """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'error': "error"
                }

        # Realiza la petición sin indicar el teléfono
        response = self.client.post(URL, data=data)
        data = response.data

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data["Mensaje"], "Debe indicar el número de teléfono.")

    def test_003_modificar_perfil(self):
        """Error en la modificación del perfil al indicar un teléfono inválido """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'tlf': "22"
                }

        # Realiza la petición con un número erróneo
        response = self.client.post(URL, data=data)
        data = response.data

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data["Mensaje"], "Error al modificar el perfil. Número de teléfono erróneo.")

    def test_004_modificar_perfil(self):
        """Error en la modificación del perfil al no estar autenticado """

        data = {'tlf': "222222222"
                }

        # Realiza la petición sin estar autenticado
        response = self.client.post(URL, data=data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
