from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, UsuarioSistema, Tarifa, Contrato, Administrador
from pagosPayPal.models import Pagos
from dateutil.relativedelta import relativedelta
from django.utils import timezone
URL = '/cibiuam/renovar_contrato/'
PAGO = '/cibiuam/pagar_renovacion/'


class RenovacionAPITest(TransactionTestCase):
    """Prueba la renovación del contrato del usuario"""
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
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(
            days=6*30), fin=timezone.localtime().date()-relativedelta(days=1), usuario=self.user, tarifa=self.semestral)

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)
        Pagos.objects.create(order_id="0AS21963LF182980A", pagado=False)

    def test_000_renovar_contrato(self):
        """Renueva el contrato correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'tarifa': "mensual"
                }

        # Realiza la petición correctamente
        response = self.client.post(URL, data)

        # Comprueba que devuelve el order_id del pago, el user_id del usuario a renovar y el importe de la renovación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("importe", response.data)

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 1,
                'tarifa': 'mensual'
                }

        # Realiza la captura de pago correctamente
        response = self.client.post(PAGO, data)

        # Comprueba que se ha creado un nuevo contrato con la tarifa deseada
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Mensaje"],
                         "Contrato renovado con éxito.")
        self.assertEqual(self.user.contratos.order_by(
            "-fin").first().inicio, timezone.localtime().date())
        self.assertEqual(self.user.contratos.order_by(
            "-fin").first().fin, timezone.localtime().date()+relativedelta(days=29))

    def test_001_renovar_contrato(self):
        """Renueva el contrato de forma errónea al no ser un usuario """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)
        data = {'tarifa': "mensual"
                }
        # Realiza la petición sin ser usuario
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un usuario.")

    def test_002_renovar_contrato(self):
        """Renueva el contrato de forma errónea al no incluir la tarifa deseada """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'error': "error"
                }

        # Realiza la petición sin indicar la tarifa
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["Mensaje"], "Debe indicar la tarifa que desea contratar.")

    def test_003_renovar_contrato(self):
        """Renueva el contrato de forma errónea al no incluir una tarifa existente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'tarifa': "error"
                }

        # Realiza la petición con una tarifa no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "Debe indicar una tarifa válida.")

    def test_004_renovar_contrato(self):
        """Error en el pago de la renovación del contrato al no ser un usuario """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Error en la captura del pago al no ser usuario
        response = self.client.post(PAGO)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un usuario.")

    def test_005_renovar_contrato(self):
        """Error en el pago de la renovación al no incluir todos los datos para proceder al pago """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 1
                }

        # Error en la captura del pago al no incluir tarifa deseada
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["Mensaje"], "Debe indicar la tarifa que desea contratar.")

        data = {
            'user_id': 1,
            'tarifa': 'mensual'
        }

        # Error en la captura del pago al no incluir order_id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "No se ha recibido order id.")

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'tarifa': 'mensual'
                }

        # Error en la captura del pago al no incluir user_id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "No se ha recibido user id.")

    def test_006_renovar_contrato(self):
        """Error en el pago de la renovación del contrato al no incluir una tarifa existente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 1,
                'tarifa': 'error'
                }

        # Error en la captura del pago al no indicar tarifa existente
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["Mensaje"],
                         "Debe indicar una tarifa válida.")

    def test_007_renovar_contrato(self):
        """Error en el pago de la renovación al indicar un user id erróneo """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 15,
                'tarifa': 'mensual'
                }

        # Error en la captura del pago al indicar user_id incorrecto
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "User id no encontrado.")

    def test_008_renovar_contrato(self):
        """Error en el pago de la renovación al indicar un order id erróneo """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'order_id': "7FS50670S",
                'user_id': 1,
                'tarifa': 'mensual'
                }
        # Error en la captura del pago al indicar order_id incorrecto
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Error"),
                         "Ocurrió un error al procesar el pago")

    def test_009_renovar_contrato(self):
        """Error en el pago de la renovación al no estar autenticado """

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'user_id': 1,
                'tarifa': 'mensual'
                }

        # Error en la captura del pago al no estar autenticado
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
