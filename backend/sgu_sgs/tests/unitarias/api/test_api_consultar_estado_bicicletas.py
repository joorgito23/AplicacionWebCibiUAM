from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, Administrador, UsuarioSistema, Estacion, Anclaje, Bicicleta, Usuario, Contrato, Tarifa
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
URL = '/cibiuam/consultar_estado_bicicleta/'


class ConsultarEstadoBicicletaAPITest(TransactionTestCase):
    """Prueba la consulta del estado de una bicicleta del campus"""
    reset_sequences = True

    def setUp(self):

        self.client = APIClient()
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.est, numAnclaje=2)
        self.bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        self.usuario = UsuarioSistema(
            username="gestorPrueba",
            rol="gestor")
        self.usuario.set_password("contragestor")
        self.usuario.save()
        self.gestorPrueba = Gestor.objects.create(
            usuario=self.usuario, nombre="luis", apellidos="perez")

        self.usuario2 = UsuarioSistema(
            username="admin",
            rol="administrador")
        self.usuario2.set_password("contraadmin")
        self.usuario2.save()
        self.admin = Administrador.objects.create(
            usuario=self.usuario2)

        self.usuario3 = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario3.set_password("contrausuario")
        self.usuario3.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario3, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=179), usuario=self.user, tarifa=self.tarifa)

        self.est2 = Estacion.objects.create(
            nombre="Prueba2", ubicacion="Calle Sevilla", latitud=2,
            longitud=2.5, nAnclajes=2)
        self.est2.crearAnclajes()

    def test_000_consultar_estado_bicicleta(self):
        """Consultar estado de bicicleta correctamente """

        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)

        # Caso en el que la bicicleta no tiene reservas previas y está en su anclaje inicial
        data = {'id': 1
                }
        # Realiza la petición con los datos correctos
        response = self.client.post(URL, data)

        # Comprueba que el estado de la bicicleta es el esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(
            "Mensaje"), "Bicicleta ubicada en el anclaje número 1 de la estación Prueba.")

        # Caso en el que la bicicleta tiene reservas y está en el anlcaje destino de la última reserva previa al momento actual
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=100), fechaFin=timezone.localtime()-relativedelta(minutes=85), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.est.getAnclajeByNumAnclaje(1), ancDestino=self.est2.getAnclajeByNumAnclaje(1), bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() - timedelta(minutes=100))

        data = {'id': 1
                }
        # Realiza la petición con los datos correctos
        response = self.client.post(URL, data)

        # Comprueba que el estado de la bicicleta es el esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(
            "Mensaje"), "Bicicleta ubicada en el anclaje número 1 de la estación Prueba2.")
        reserva.delete()

        # Caso en el que la bicicleta está en uso actualmente
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=10), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.est.getAnclajeByNumAnclaje(1), ancDestino=self.est2.getAnclajeByNumAnclaje(1), bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() - timedelta(minutes=100))

        data = {'id': 1
                }
        # Realiza la petición con los datos correctos
        response = self.client.post(URL, data)

        # Comprueba que el estado de la bicicleta es el esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(
            "Mensaje"), "Bicicleta en uso.")

    def test_001_consultar_estado_bicicleta(self):
        """Consultar estado de bicicleta de forma errónea al no indicar id de bicicleta """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'error': "error"
                }

        # Realiza la petición sin indicar id de bicicleta
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Debe indicar la bicicleta.")

    def test_002_consultar_estado_bicicleta(self):
        """Consultar estado de bicicleta de forma errónea al indicar un id de bicicleta no existente"""
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario)
        data = {'id': 5
                }

        # Realiza la petición con un id no existente
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Bicicleta no encontrada.")

    def test_003_consultar_estado_bicicleta(self):
        """Consultar estado de bicicleta de forma errónea al no estar identificado """

        data = {'id': 1
                }

        # Realiza la petición sin identificarse
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_004_consultar_estado_bicicleta(self):
        """Consultar estado de bicicleta de forma errónea al no ser un gestor """
        # Autentica al usuario
        self.client.force_authenticate(user=self.usuario2)

        data = {'id': 1
                }

        # Realiza la petición sin ser gestor
        response = self.client.post(URL, data)

        # Verificación acciones y respuestas esperadas
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("Mensaje"), "Debes ser un gestor.")
