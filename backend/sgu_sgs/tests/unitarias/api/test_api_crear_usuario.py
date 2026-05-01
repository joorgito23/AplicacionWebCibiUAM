from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, UsuarioPendiente, UsuarioSistema, Tarifa
from pagosPayPal.models import Pagos
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
URL = '/cibiuam/crear_usuario/'
PAGO = '/cibiuam/pagar/'


class CrearUsuarioAPITest(TransactionTestCase):
    """Prueba la creación de usuarios"""
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
        Pagos.objects.create(order_id="3XR38212DF879261C", pagado=False)

    def test_000_crear_usuario(self):
        """Crea un nuevo usuario pendiente de pago correctamente """

        data = {'usuario': "usuario",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrauser",
                'tlf': "111111111",
                'tarifa': "mensual"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Comprueba que devuelve el order_id del pago, el importe y el user_id del usuario pendiente creado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("importe", response.data)
        self.assertEqual(response.data.get("importe"), float(10))
        self.assertIn("fin", response.data)
        self.assertEqual(response.data.get("fin"), str(
            timezone.localtime().date()+relativedelta(days=29)))

    def test_001_crear_usuario(self):
        """Error en la creación de un nuevo usuario al indicar un número de teléfono erróneo """

        data = {'usuario': "usuario",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrauser",
                'tlf': "11111",
                'tarifa': "mensual"
                }

        # Realiza la petición con teléfono erróneo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_002_crear_usuario(self):
        """Error en la creación de un nuevo usuario al indicar una contraseña muy corta """

        data = {'usuario': "usuario",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "usuario",
                'tlf': "111111111",
                'tarifa': "mensual"
                }

        # Realiza la petición con contraseña insegura
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errores"].get("contraseña")[
                         0], "La contraseña no cumple los requisitos de seguridad")

    def test_003_crear_usuario(self):
        """Error en la creación de un nuevo usuario al indicar un nombre de usuario ya existente """

        # Creación usuario
        UsuarioPendiente.objects.create(usuario="prueba", nombre="Prueba", apellidos="prueba",
                                        contraseña="contrapago", tlf="111111111", tarifa=self.anual, expires_at=timezone.localtime() + timedelta(minutes=10))
        usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        usuario.set_password("contrausuario")
        usuario.save()
        Usuario.objects.create(
            usuario=usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

        data = {'usuario': "usuario",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrausuario",
                'tlf': "111111111",
                'tarifa': "mensual"
                }

        # Realiza la petición con usuario ya existente a un usuario pendiente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errores"].get("usuario")[
                         0], "El nombre de usuario ya existe")

        data = {'usuario': "prueba",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrausuario",
                'tlf': "111111111",
                'tarifa': "mensual"
                }

        # Realiza la petición con usuario ya existente a un usuario
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["errores"].get("usuario")[
                         0]), "usuario pendiente with this usuario already exists.")

    def test_004_crear_usuario(self):
        """Error en la creación de un nuevo usuario al indicar una tarifa no existente"""

        data = {'usuario': "usuario2",
                'nombre': "Pepe",
                'apellidos': "Perez Rodriguez",
                'contraseña': "contrausuario",
                'tlf': "111111111",
                'tarifa': "error"
                }

        # Realiza la petición con una tarifa no válida
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errores"].get(
            "tarifa")[0], "Tarifa no existente")

    def test_005_pagar(self):
        """Pagar el alta de una cuenta de manera correcta con un order id correcto"""

        # Crea un usuario pendiente
        UsuarioPendiente.objects.create(usuario="prueba", nombre="Prueba", apellidos="prueba",
                                        contraseña="contrapago", tlf="111111111", tarifa=self.anual, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="3XR38212DF879261C").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "3XR38212DF879261C",
                'user_id': 1
                }
        # Procede a la captura del pago correctamente tras su aprobación
        response = self.client.post(PAGO, data)

        # Comprueba que el usuario se haya creado y se haya eliminado el usuario pendiente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuarioSistema = UsuarioSistema.objects.filter(
            username="prueba").first()
        self.assertEqual(Usuario.objects.filter(
            usuario=usuarioSistema).exists(), True)
        self.assertEqual(UsuarioPendiente.objects.filter(
            usuario="prueba").exists(), False)
        self.assertEqual(response.data["Mensaje"], "Usuario creado con éxito.")

    def test_006_pagar(self):
        """Pago erróneo al no indicar order id ni user id"""

        data = {'error': "rr",
                'user_id': 1
                }
        # Procede a capturar el pago de forma errónea sin indicar order id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "No se ha recibido order id.")

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="3XR38212DF879261C").first()
        estado.pagado = False
        estado.save()

        data = {'error': "rr",
                'order_id': "3XR38212DF879261C"
                }
        # Procede a capturar el pago de forma errónea sin indicar user id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "No se ha recibido user id.")

    def test_007_pagar(self):
        """Pago erróneo al pasar un user id erróneo"""

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="3XR38212DF879261C").first()
        estado.pagado = False
        estado.save()
        data = {'order_id': "3XR38212DF879261C",
                'user_id': 145
                }
        # Procede a capturar el pago de forma errónea al indicar user id erróneo
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"], "User id no encontrado.")

    def test_008_pagar(self):
        """Pago erróneo al pasar un order id erróneo"""

        data = {'order_id': "3NR567451C",
                'user_id': 2
                }
        # Procede a capturar el pago de forma errónea al indicar order id erróneo
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Error"),
                         "Ocurrió un error al procesar el pago")
