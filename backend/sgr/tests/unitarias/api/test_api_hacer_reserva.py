from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Administrador, Contrato, Estacion, Bicicleta, Anclaje, UsuarioSistema, Tarifa, Notificacion
from pagosPayPal.models import Pagos
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
URL = '/cibiuam/hacer_reserva/'
PAGO = '/cibiuam/pagar_reserva/'


class HacerReservaAPITest(TransactionTestCase):
    """Prueba la realización de reservas por un usuario"""
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
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=179), usuario=self.user, tarifa=self.semestral)

        self.est = Estacion.objects.create(
            nombre="Estación 1", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.est, numAnclaje=2)
        self.bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        self.est2 = Estacion.objects.create(
            nombre="Estación 2", ubicacion="Prueba2", latitud=3,
            longitud=0.5, nAnclajes=2)
        self.anc3 = Anclaje.objects.create(estacion=self.est2, numAnclaje=1)
        self.anc4 = Anclaje.objects.create(estacion=self.est2, numAnclaje=2)
        Pagos.objects.create(order_id="0AS21963LF182980A", pagado=False)

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

    def test_000_hacer_reserva(self):
        """Realiza una nueva reserva pendiente de pago correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 1"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Comprueba que devuelve el order_id del pago, el importe y la información de la reserva deseada
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertIn("reserva_id", response.data)
        self.assertIn("importe", response.data)
        self.assertEqual(response.data.get("importe"), float(0.1))
        self.assertIn("inicio", response.data)
        self.assertIn("fin", response.data)
        self.assertIn("horaFin", response.data)
        self.assertIn("horaInicio", response.data)
        self.assertIn("origen", response.data)
        self.assertIn("destino", response.data)
        self.assertEqual(Reserva.objects.filter(
            id=response.data['reserva_id']).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=response.data['reserva_id']).first().estado, 'pendiente')

    def test_001_hacer_reserva(self):
        """Realiza una nueva reserva pendiente de pago correctamente y el usuario tiene saldo"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        self.user.saldo = 5
        self.user.save()

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Comprueba que realiza la reserva directamente al no tener coste
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("importe", response.data)
        self.assertEqual(response.data.get("importe"), float(0))
        self.assertIn("Mensaje", response.data)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva realizada con éxito.")
        self.assertEqual(Reserva.objects.filter(
            id=response.data['reserva_id']).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=response.data['reserva_id']).first().estado, 'pagada')

    def test_002_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no estar autenticado"""

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_003_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no ser usuario"""
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un usuario.")

    def test_004_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no indicar todos los datos necesarios"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {
            'fin': str(timezone.localtime().date()),
            'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
            'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
            'origen': "Estación 1",
            'destino': "Estación 2"
        }

        # Realiza la petición sin fecha de inicio
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }
        # Realiza la petición sin fecha de fin
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición sin hora de inicio
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición sin hora de fin
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'destino': "Estación 2"
                }

        # Realiza la petición sin origen
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1"
                }

        # Realiza la petición sin destino
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar todos los campos necesarios.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_005_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar una estación no existente"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Error 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con estación origen no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Estación origen no existente.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Error 2"
                }

        # Realiza la petición con estación destino no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Estación destino no existente.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_006_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar fecha u hora con formato erróneo"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': "01-01-2020",
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con formato erróneo para la fecha
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Formato de fecha incorrecto. Usa YYYY-MM-DD")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': "error",
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con formato erróneo para la hora
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Formato de hora incorrecto. Usa horas:minutos")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_007_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no disponer el usuario de un contrato activo"""

        # Creamos usuario sin contrato
        usuario = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        usuario.set_password("contrausuario")
        usuario.save()
        Usuario.objects.create(
            usuario=usuario, nombre="Sin contrato", apellidos="Prueba", saldo=0.0, tlf="111111111")

        # Autentica al usuario
        self.client.force_authenticate(user=usuario)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición sin contrato
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes disponer de un contrato activo para realizar reservas.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_008_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar fechas anteriores al momento actual"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': str(timezone.localtime().date()-relativedelta(days=2)),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con fecha anterior al momento actual
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes introducir fechas posteriores al momento actual.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_009_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar fecha de inicio posterior a la de fin"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': str(timezone.localtime().date()+relativedelta(days=2)),
                'fin': str(timezone.localtime().date()+relativedelta(days=2)),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con fecha de inicio posterior a fecha de fin
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "La fecha de inicio debe ser anterior a la de fin.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_010_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar fechas fuera del periodo del contrato activo"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'inicio': str(timezone.localtime().date()+relativedelta(days=200)),
                'fin': str(timezone.localtime().date()+relativedelta(days=200)),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición con fechas fuera del contrato activo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes realizar la reserva en el periodo de tu contrato activo.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_011_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al indicar fechas coincidentes con otra reserva previa"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=20)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición coincidente con otra reserva existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Ya dispones de una reserva en esa franja horaria.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_012_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no haber bicicletas disponibles en la estación de origen deseada"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=50)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=55)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No es posible realizar una reserva con las condiciones deseadas.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_013_hacer_reserva(self):
        """Realiza una nueva reserva de forma errónea al no haber anclajes disponibles en la estación de destino deseada"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos bicicletas en la estación destino para ocupar anclajes
        Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc4)
        Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc3)

        data = {'inicio': str(timezone.localtime().date()),
                'fin': str(timezone.localtime().date()),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=50)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=55)).time()),
                'origen': "Estación 1",
                'destino': "Estación 2"
                }

        # Realiza la petición
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No es posible realizar una reserva con las condiciones deseadas.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_014_pagar_reserva(self):
        """Realiza el pago de una reserva pendiente de pago correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva pendiente de pago
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0.1, estado='pendiente',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 1,
                'saldo': 0
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(PAGO, data)

        # Comprueba que se realiza la reserva y se envía la notificación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva realizada con éxito.")
        self.assertEqual(Reserva.objects.filter(id=r.id).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=r.id).first().estado, 'pagada')
        self.assertEqual(Notificacion.objects.filter(
            usuario=self.user, msg=f"A continuación se indica un resumen de su reserva. Inicio: {timezone.localtime(r.fechaInicio).strftime("%Y-%m-%d %H:%M")} - Fin: {timezone.localtime(r.fechaFin).strftime("%Y-%m-%d %H:%M")}. Origen: {r.estOrigen.nombre} nº {r.ancOrigen.numAnclaje} - Destino: {r.estDestino.nombre} nº {r.ancDestino.numAnclaje}. Código de recogida: {r.codigoRecogida}").exists(), True)

    def test_015_pagar_reserva(self):
        """Realiza el pago de una reserva pendiente de pago correctamente y descuenta saldo al usuario"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva pendiente de pago
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0.1, estado='pendiente',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Simulamos que no se ha pagado todavía
        estado = Pagos.objects.filter(order_id="0AS21963LF182980A").first()
        estado.pagado = False
        estado.save()
        self.user.saldo = 5
        self.user.save()

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': r.id,
                'saldo': -0.1
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(PAGO, data)

        # Comprueba que realiza la reserva, descuenta saldo y envía notificación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva realizada con éxito.")
        self.assertEqual(Reserva.objects.filter(id=r.id).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=r.id).first().estado, 'pagada')
        self.assertEqual(self.user.saldo, 4.9)
        self.assertEqual(Notificacion.objects.filter(
            usuario=self.user, msg=f"A continuación se indica un resumen de su reserva. Inicio: {timezone.localtime(r.fechaInicio).strftime("%Y-%m-%d %H:%M")} - Fin: {timezone.localtime(r.fechaFin).strftime("%Y-%m-%d %H:%M")}. Origen: {r.estOrigen.nombre} nº {r.ancOrigen.numAnclaje} - Destino: {r.estDestino.nombre} nº {r.ancDestino.numAnclaje}. Código de recogida: {r.codigoRecogida}").exists(), True)

    def test_016_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al no estar autenticado"""

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 1,
                'saldo': -2
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_017_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al no ser usuario"""
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 1,
                'saldo': -2
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un usuario.")

    def test_018_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al no indicar todos los datos necesarios"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {
            'reserva_id': 1,
            'saldo': -2
        }

        # Realiza la petición sin order_id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No se ha recibido order id.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'order_id': "0AS21963LF182980A",
                'saldo': -2
                }

        # Realiza la petición sin reserva id
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No se ha recibido reserva id.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 1
                }

        # Realiza la petición sin saldo
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No se ha recibido saldo a descontar.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_019_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al indicar saldo o reserva id erróneo"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': "error",
                'saldo': -2
                }

        # Realiza la petición con reserva id erróneo
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva id con formato erróneo.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 1,
                'saldo': "error"
                }

        # Realiza la petición con saldo erróneo
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Saldo con formato erróneo.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_020_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al indicar una reserva no existente"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': 5,
                'saldo': -2
                }

        # Realiza la petición con reserva id no existente
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva no existente.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_021_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al indicar una reserva expirada"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva pendiente de pago
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0.1, estado='pendiente',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() - timedelta(minutes=10))

        data = {'order_id': "0AS21963LF182980A",
                'reserva_id': r.id,
                'saldo': -0.1
                }

        # Realiza la petición
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva expirada.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_022_pagar_reserva(self):
        """Intenta pagar una reserva de forma errónea al indicar un order id inválido"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva pendiente de pago
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0.1, estado='pendiente',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'order_id': "0K03804730V",
                'reserva_id': r.id,
                'saldo': -0.1
                }
        # Error en la captura del pago al indicar order_id incorrecto
        response = self.client.post(PAGO, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Error"),
                         "Ocurrió un error al procesar el pago")
