from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Contrato
from pagosPayPal.models import Pagos
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Intregacion_2_Test(TransactionTestCase):
    """Test de integración 2
        Realiza las acciones de un usuario que desea utilizar la app:
        - Realiza login
        - Consultar su perfil
        - Actualizar su número de teléfono
        - Leer las notificaciones pendientes de lectura
        - Renovar su contrato tras leer que le quedan menos de 10 días
        - Realiza logout
    """
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

        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Luis", apellidos="Perez Perez", saldo=0.0, tlf="111111111")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=self.user, tarifa=self.mensual)
        Pagos.objects.create(order_id="3XR38212DF879261C", pagado=False)

    def test_integracion_2(self):
        # Iniciamos sesión
        data = {'username': "usuario",
                "password": "contrausuario"
                }

        # Realiza la petición correctamente con credenciales de un usuario
        response = self.client.post('/auth/token/login', data={'username': "usuario",
                                                               "password": "contrausuario"
                                                               })

        token = response.data.get("auth_token")

        # Consultamos perfil del usuario

        # Realiza la petición correctamente con credenciales de un usuario
        response = self.client.get(
            '/cibiuam/consultar_perfil/', headers={'Authorization': f'Token {token}'})

        data = response.data

        # Comprueba que devuelve todos los datos correctos
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["usuario"], "usuario")
        self.assertEqual(data["nombre"], "Luis")
        self.assertEqual(data["apellidos"], "Perez Perez")
        self.assertEqual(data["rol"], "usuario")
        self.assertEqual(data["duracion"], "Mensual")
        self.assertEqual(
            data["fin"], timezone.localtime(
            ).date()-relativedelta(days=25)+relativedelta(days=29))
        self.assertEqual(data["saldo"], 0.0)
        self.assertEqual(data["tlf"], "111111111")

        # Actualizamos teléfono

        data = {'tlf': "222222222"
                }

        # Realiza la petición correctamente
        response = self.client.post(
            '/cibiuam/modificar_perfil/', data=data, headers={'Authorization': f'Token {token}'})
        data = response.data

        # Comprueba que se haya actualizado el teléfono
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["Mensaje"], "Datos actualizados correctamente.")
        self.assertEqual(Usuario.objects.filter(
            usuario=self.usuario).first().tlf, "222222222")

        # Leemos notificaciones

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/leer_notificaciones/', headers={'Authorization': f'Token {token}'})
        data = response.data

        # Comprueba que recibe todas las notificaciones no leídas del usuario
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fecha"], str(timezone.localtime().date(
        )-relativedelta(days=25)+relativedelta(days=29)-relativedelta(days=10)))
        self.assertEqual(
            data[0]["msg"], "Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.")

        # Comprueba que no recibe ninguna notificación tras haber leído todas previamente
        response = self.client.get(
            '/cibiuam/leer_notificaciones/', headers={'Authorization': f'Token {token}'})
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)

        # Renueva el contrato para seguir usando el servicio

        data = {'tarifa': "anual"
                }

        # Realiza la petición correctamente
        response = self.client.post(
            '/cibiuam/renovar_contrato/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve el order_id del pago, el user_id del usuario a renovar y el importe de la renovación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("importe", response.data)
        self.assertEqual(response.data.get("importe"), float(8))

        data = {'order_id': "3XR38212DF879261C",
                'user_id': 1,
                'tarifa': 'anual'
                }

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="3XR38212DF879261C").first()
        estado.pagado = False
        estado.save()

        # Realiza la captura de pago correctamente
        response = self.client.post(
            '/cibiuam/pagar_renovacion/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que se ha creado un nuevo contrato con la tarifa deseada
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Mensaje"],
                         "Contrato renovado con éxito.")
        self.assertEqual(self.user.contratos.order_by(
            "-fin").first().inicio, timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29)+relativedelta(days=1))
        self.assertEqual(self.user.contratos.order_by(
            "-fin").first().fin, timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29)+relativedelta(days=1)+relativedelta(days=12*30 - 1))

        # Realiza logout
        response = self.client.post(
            '/auth/token/logout', headers={'Authorization': f'Token {token}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
