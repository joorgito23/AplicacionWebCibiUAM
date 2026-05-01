from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import UsuarioSistema, Tarifa, Estacion, Anclaje, Bicicleta, Usuario, Contrato
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Intregacion_6_Test(TransactionTestCase):
    """Test de integración 6
        Realiza las acciones de un usuario que desea cancelar una reserva:
        - Realiza login
        - Realiza una reserva con una fecha que no era la deseada
        - Consulta sus reservas para ver el id de la reserva realizada para cancelarla
        - Cancela la reserva
        - Quiere volver a cancelarla por si acaso y da error
        - Cierra sesión
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

        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Luis", apellidos="Perez Perez", saldo=0.0, tlf="111111111")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=self.user, tarifa=self.mensual)

    def test_integracion_6(self):
        # Iniciamos sesión

        # Realiza la petición de login correctamente con las credenciales de un usuario
        response = self.client.post('/auth/token/login', data={'username': "usuario",
                                                               "password": "contrausuario"
                                                               })

        token = response.data.get("auth_token")

        # Realiza una reserva con una fecha mal introducida por error
        data = {'inicio': str(timezone.localtime().date()+relativedelta(days=1)),
                'fin': str(timezone.localtime().date()+relativedelta(days=1)),
                'horaInicio': str((timezone.localtime()+relativedelta(minutes=30)).time()),
                'horaFin': str((timezone.localtime()+relativedelta(minutes=40)).time()),
                'origen': "Facultad de Formación de Profesorado y Educación",
                'destino': "EPS"
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(
            '/cibiuam/hacer_reserva/', headers={'Authorization': f'Token {token}'}, data=data)

        # Comprueba que realiza la reserva directamente al no tener coste por tener la tarifa mensual
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
        r = Reserva.objects.filter(id=response.data['reserva_id']).first()

        # Consulta sus reservas

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/consultar_reservas/', headers={'Authorization': f'Token {token}'})

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(timezone.localtime(r.fechaInicio).strftime(
            "%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual(timezone.localtime(r.fechaFin).strftime(
            "%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(r.codigoRecogida, response.data[0].get(
            "codigoRecogida"))
        self.assertEqual(0, response.data[0].get(
            "importe"))
        self.assertEqual("pagada", response.data[0].get(
            "estado"))
        self.assertEqual("Facultad de Formación de Profesorado y Educación", response.data[0].get(
            "estOrigen").get("nombre"))
        self.assertEqual("EPS", response.data[0].get(
            "estDestino").get("nombre"))
        self.assertEqual(r.ancOrigen.numAnclaje, response.data[0].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(r.ancDestino.numAnclaje, response.data[0].get(
            "ancDestino").get("numAnclaje"))

        # Cancela la reserva una vez conoce el id
        data = {'reserva_id': r.id,
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(
            '/cibiuam/cancelar_reserva/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que cancela la reserva correctamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva cancelada con éxito.")
        self.assertEqual(Reserva.objects.filter(
            id=r.id).exists(), True)
        self.assertEqual(Reserva.objects.filter(
            id=r.id).first().estado, 'cancelada')

        # Trata de volver a cancelarla con error
        data = {'reserva_id': r.id,
                }

        # Realiza la petición con todos los datos necesarios
        response = self.client.post(
            '/cibiuam/cancelar_reserva/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que la reserva no se puede cancelar
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("Mensaje"),
                         "Reserva no cancelable.")

        # Realiza logout
        response = self.client.post(
            '/auth/token/logout', headers={'Authorization': f'Token {token}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
