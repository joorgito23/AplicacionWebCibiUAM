from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Usuario, Gestor, Administrador, Contrato, Estacion, Bicicleta, Anclaje, UsuarioSistema, Tarifa
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
URL = '/cibiuam/consultar_reservas/'


class ConsultarReservasAPITest(TransactionTestCase):
    """Prueba la consulta de reservas para usuarios y gestores"""
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

        self.usuario3 = UsuarioSistema(
            username="gestor",
            rol="gestor")
        self.usuario3.set_password("contragestor")
        self.usuario3.save()
        self.gestor = Gestor.objects.create(
            usuario=self.usuario3)

        self.usuario4 = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        self.usuario4.set_password("contrausuario")
        self.usuario4.save()
        self.user2 = Usuario.objects.create(
            usuario=self.usuario4, nombre="Prueba", apellidos="Prueba", saldo=5.0, tlf="111111111")

        self.r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=20), importe=0.01, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.r2 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=50), fechaFin=timezone.localtime()+relativedelta(minutes=60), importe=0.01, estado='pendiente',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.r3 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=30), fechaFin=timezone.localtime()+relativedelta(minutes=40), importe=0.01, estado='pagada',
                                         estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=self.bici, usuario=self.user2, expires_at=timezone.localtime() + timedelta(minutes=10))

    def test_000_consultar_reservas(self):
        """Consultar las reservas correctamente por un usuario """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=20)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r1.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.01, response.data[0].get(
            "importe"))
        self.assertEqual("pagada", response.data[0].get(
            "estado"))
        self.assertEqual("Estación 1", response.data[0].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 2", response.data[0].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[0].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[0].get(
            "ancDestino").get("numAnclaje"))

    def test_001_consultar_reservas(self):
        """Consultar las reservas correctamente por un gestor """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario3)

        # Realiza la petición correctamente
        response = self.client.get(URL)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=20)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaFin"))
        self.assertEqual(self.r1.codigoRecogida, response.data[1].get(
            "codigoRecogida"))
        self.assertEqual(0.01, response.data[1].get(
            "importe"))
        self.assertEqual("pagada", response.data[1].get(
            "estado"))
        self.assertEqual("Estación 1", response.data[1].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 2", response.data[1].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[1].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[1].get(
            "ancDestino").get("numAnclaje"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=30)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(minutes=40)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[0].get(
            "codigoRecogida"))
        self.assertEqual(0.01, response.data[0].get(
            "importe"))
        self.assertEqual("pagada", response.data[0].get(
            "estado"))
        self.assertEqual("Estación 2", response.data[0].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 1", response.data[0].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[0].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[0].get(
            "ancDestino").get("numAnclaje"))

    def test_002_consultar_reservas(self):
        """Error en la consulta de las reservas al no ser un gestor o usuario"""

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        # Realiza la petición sin ser gestor ni usuario
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"),
                         "No tienes permisos para ver las reservas.")

    def test_003_consultar_reservas(self):
        """Error en la consulta de las reservas al no estar autenticado"""

        # Realiza la petición sin estar autenticado
        response = self.client.get(URL)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
