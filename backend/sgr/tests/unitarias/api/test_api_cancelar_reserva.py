from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Administrador, Contrato, Estacion, Bicicleta, Anclaje, UsuarioSistema, Tarifa
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
URL = '/cibiuam/cancelar_reserva/'


class CancelarReservaAPITest(TransactionTestCase):
    """Prueba la cancelación de reservas"""
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
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=5.0, tlf="111111111")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=self.user, tarifa=self.semestral)

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

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

    def test_000_cancelar_reserva(self):
        """Cancela una reserva correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva para poder cancelarla
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=65), fechaFin=timezone.localtime()+relativedelta(minutes=70), importe=0.05, estado='pagada',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'reserva_id': r.id}

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Comprueba que cancela la reserva correctamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva cancelada con éxito.")
        self.assertEqual(Reserva.objects.filter(
            id=r.id).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=r.id).first().estado, 'cancelada')
        self.assertEqual(self.user.saldo, 5.05)

    def test_001_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al no estar autenticado"""

        data = {'reserva_id': 1,
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_002_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al no ser usuario"""
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        data = {'reserva_id': 1,
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debes ser un usuario.")

    def test_003_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al no indicar id de reserva"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'error': 1,
                }

        # Realiza la petición sin id de reserva a cancelar
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "No se ha recibido reserva id.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_004_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al indicar formato incorrecto de id"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'reserva_id': "error",
                }

        # Realiza la petición con id erróneo
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva id con formato erróneo.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_005_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al indicar un id de reserva no existente"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        data = {'reserva_id': 50,
                }

        # Realiza la petición con id no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva no existente.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_006_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al no estar pagada"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva a cancelar sin pagar
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=65), fechaFin=timezone.localtime()+relativedelta(minutes=70), importe=0.05, estado='pendiente',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'reserva_id': r.id,
                }

        # Realiza la petición sin pagar la reserva
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva no pagada.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_007_cancelar_reserva(self):
        """Cancela una reserva de forma errónea al realizarlo con menos de una hora de antelación"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Creamos reserva a cancelar
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=20), importe=0.05, estado='pagada',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        data = {'reserva_id': r.id,
                }

        # Realiza la petición con menos de una hora de antelación
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva no cancelable.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
