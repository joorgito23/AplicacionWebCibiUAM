from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import UsuarioSistema, Tarifa, Estacion, Anclaje, Bicicleta, Usuario, UsuarioPendiente
from pagosPayPal.models import Pagos
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Intregacion_1_Test(TransactionTestCase):
    """Test de integración 1
        Realiza las acciones de un nuevo usuario que desea utilizar el servicio:
        - Consultar tarifas de la aplicación
        - Consultar estado del campus para conocer las estaciones disponibles
        - Realizar alta de usuario
        - Realizar primer inicio de sesión
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

        self.e = Estacion.objects.create(
            nombre="EPS", ubicacion="Campus de Cantoblanco, C. Francisco Tomás y Valiente, 11, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54719581685481,
            longitud=-3.691637357994746, nAnclajes=2)
        self.e.crearAnclajes()
        self.e1 = Estacion.objects.create(
            nombre="Facultad de Formación de Profesorado y Educación", ubicacion="C. Francisco Tomás y Valiente, 3, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54510026811934,
            longitud=-3.6966638957627427, nAnclajes=3)
        self.anc = Anclaje.objects.create(estacion=self.e1, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.e1, numAnclaje=2)
        self.anc3 = Anclaje.objects.create(estacion=self.e1, numAnclaje=3)
        self.bici = Bicicleta.objects.create(
            estacionInicial=self.e1, anclajeInicio=self.anc)
        Pagos.objects.create(order_id="0AS21963LF182980A", pagado=False)

    def test_integracion_1(self):
        # Obtenemos listado de tarifas

        response = self.client.get('/cibiuam/informacion/tarifas/')

        # Comprueba que devuelve el nombre de las tarifas existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get("duracion"), "mensual")
        self.assertEqual(response.data[1].get("duracion"), "semestral")
        self.assertEqual(response.data[2].get("duracion"), "anual")

        # Consultamos las 3 tarifas para ver cual nos interesa

        # Semestral
        data = {'nombre': "semestral"
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_tarifa/', data)

        # Comprueba que los datos devueltos son correctos y coinciden con los de la tarifa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("importe"), 5)
        self.assertEqual(response.data.get("precioMinuto"), 0.01)
        self.assertEqual(response.data.get(
            "descripcion"), "Esta tarifa permite realizar reservas con un coste bajo.")
        self.assertEqual(response.data.get("duracion"), "semestral")

        # Anual
        data = {'nombre': "anual"
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_tarifa/', data)

        # Comprueba que los datos devueltos son correctos y coinciden con los de la tarifa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("importe"), 8)
        self.assertEqual(response.data.get("precioMinuto"), 0.01)
        self.assertEqual(response.data.get(
            "descripcion"), "Esta tarifa permite hacer un renovacion al año y olvidarte")
        self.assertEqual(response.data.get("duracion"), "anual")

        # Mensual
        data = {'nombre': "mensual"
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_tarifa/', data)

        # Comprueba que los datos devueltos son correctos y coinciden con los de la tarifa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("importe"), 10)
        self.assertEqual(response.data.get("precioMinuto"), 0)
        self.assertEqual(response.data.get(
            "descripcion"), "Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.")
        self.assertEqual(response.data.get("duracion"), "mensual")

        # Consultamos detalles y estados de las estaciones

        data = {'estacion': "EPS"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado/', data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 2)
        self.assertEqual(response.data.get("ocupado"), 0)

        data = {'estacion': "Facultad de Formación de Profesorado y Educación"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado/', data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 2)
        self.assertEqual(response.data.get("ocupado"), 1)

        # Ubicación de estaciones

        # Realiza la petición correctamente
        response = self.client.get('/cibiuam/informacion/estaciones/')

        # Comprueba que devuelve todas las estaciones con su nombre y ubicación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("nombre"), "EPS")
        self.assertEqual(response.data[1].get(
            "nombre"), "Facultad de Formación de Profesorado y Educación")
        self.assertEqual(response.data[0].get(
            "ubicacion"), "Campus de Cantoblanco, C. Francisco Tomás y Valiente, 11, Fuencarral-El Pardo, 28049 Madrid")
        self.assertEqual(response.data[1].get(
            "ubicacion"), "C. Francisco Tomás y Valiente, 3, Fuencarral-El Pardo, 28049 Madrid")

        # Procede a darse de alta

        data = {'usuario': "usuario",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrauser",
                'tlf': "111111111",
                'tarifa': "mensual"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post('/cibiuam/crear_usuario/', data)

        # Comprueba que devuelve el order_id del pago, el importe, el user_id del usuario pendiente creado y fecha de fin de contrato
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("importe", response.data)
        self.assertEqual(response.data.get("importe"), float(10))
        self.assertIn("fin", response.data)
        self.assertEqual(response.data.get("fin"), str(
            timezone.localtime().date()+relativedelta(days=29)))

        # Procede a pagar
        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 1
                }
        # Procede a la captura del pago correctamente tras su aprobación
        response = self.client.post('/cibiuam/pagar/', data)

        # Comprueba que el usuario se haya creado y se haya eliminado el usuario pendiente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuarioSistema = UsuarioSistema.objects.filter(
            username="usuario").first()
        self.assertEqual(Usuario.objects.filter(
            usuario=usuarioSistema).exists(), True)
        self.assertEqual(UsuarioPendiente.objects.filter(
            usuario="usuario").exists(), False)
        self.assertEqual(response.data["Mensaje"], "Usuario creado con éxito.")

        # Realiza login tras alta de usuario

        data = {'username': "usuario",
                "password": "contrauser"
                }

        # Realiza la petición correctamente con credenciales de un usuario
        response = self.client.post('/auth/token/login', data)

        # Comprueba que el login es correcto y devuelve el token y el rol
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("auth_token", response.data)
        self.assertEqual("usuario", response.data.get("rol"))

        # Realiza logout
        response = self.client.post(
            '/auth/token/logout', headers={'Authorization': f'Token {response.data.get("auth_token")}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
