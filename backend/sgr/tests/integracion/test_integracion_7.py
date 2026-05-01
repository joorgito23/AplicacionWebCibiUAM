from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, UsuarioSistema, Tarifa, Estacion, Anclaje, Bicicleta, Usuario, Contrato
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta


class Intregacion_7_Test(TransactionTestCase):
    """Test de integración 7
        Realiza las acciones de un gestor que desea consultar el historial de reservas de los usuarios para gestionar el servicio:
        - Realiza login
        - Consulta el historial de reservas
        - Filtra las reservas para analizar la demanda
        - Crea una nueva estación en una zona transitada
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
            username="gestor",
            rol="gestor")
        self.usuario2.set_password("contragestor")
        self.usuario2.save()
        self.gestor = Gestor.objects.create(
            usuario=self.usuario2)

        self.usuario3 = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        self.usuario3.set_password("contrausuario")
        self.usuario3.save()
        self.user2 = Usuario.objects.create(
            usuario=self.usuario3, nombre="Prueba", apellidos="Prueba", saldo=5.0, tlf="111111111")

        self.r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=1), fechaFin=timezone.localtime()+relativedelta(days=1, minutes=10), importe=0.1, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.r2 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=3), fechaFin=timezone.localtime()+relativedelta(days=3, minutes=10), importe=0.1, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.r3 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2), fechaFin=timezone.localtime()+relativedelta(days=2, minutes=10), importe=0.1, estado='pagada',
                                         estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=self.bici, usuario=self.user2, expires_at=timezone.localtime() + timedelta(minutes=10))

    def test_integracion_7(self):
        # Iniciamos sesión
        data = {'username': "gestor",
                "password": "contragestor"
                }

        # Realiza la petición de login correctamente con las credenciales de un usuario
        response = self.client.post('/auth/token/login', data=data)

        token = response.data.get("auth_token")

        # Consulta las reservas

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/consultar_reservas/', headers={'Authorization': f'Token {token}'})

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual("usuario", response.data[2].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[2].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[2].get("fechaFin"))
        self.assertEqual(self.r1.codigoRecogida, response.data[2].get(
            "codigoRecogida"))
        self.assertEqual(0.1, response.data[2].get(
            "importe"))
        self.assertEqual("pagada", response.data[2].get(
            "estado"))
        self.assertEqual("Estación 1", response.data[2].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 2", response.data[2].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[2].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[2].get(
            "ancDestino").get("numAnclaje"))

        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r2.codigoRecogida, response.data[0].get(
            "codigoRecogida"))
        self.assertEqual(0.1, response.data[0].get(
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

        self.assertEqual("usuario2", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[1].get(
            "codigoRecogida"))
        self.assertEqual(0.1, response.data[1].get(
            "importe"))
        self.assertEqual("pagada", response.data[1].get(
            "estado"))
        self.assertEqual("Estación 2", response.data[1].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 1", response.data[1].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[1].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[1].get(
            "ancDestino").get("numAnclaje"))

        # Filtra las reservas para analizar la demanda

        # Filtramos por fecha de inicio
        data = {'inicio': str(timezone.localtime().date()+relativedelta(days=2))
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_reservas_filtros/', headers={
                                    'Authorization': f'Token {token}'}, data=data)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r2.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[0].get(
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("usuario2", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[1].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[1].get(
            "importe"))
        self.assertEqual("pagada", response.data[1].get(
            "estado"))
        self.assertEqual("Estación 2", response.data[1].get(
            "estOrigen").get("nombre"))
        self.assertEqual("Estación 1", response.data[1].get(
            "estDestino").get("nombre"))
        self.assertEqual(1, response.data[1].get(
            "ancOrigen").get("numAnclaje"))
        self.assertEqual(1, response.data[1].get(
            "ancDestino").get("numAnclaje"))

        # Filtramos por fecha de fin
        data = {'fin': str(timezone.localtime().date()+relativedelta(days=2))
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_reservas_filtros/', headers={
                                    'Authorization': f'Token {token}'}, data=data)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaFin"))
        self.assertEqual(self.r1.codigoRecogida, response.data[1].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[1].get(
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
        self.assertEqual((timezone.localtime()+relativedelta(days=2)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[0].get(
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

        # Filtramos por destino
        data = {'destino': "Estación 1",
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_reservas_filtros/', headers={
                                    'Authorization': f'Token {token}'}, data=data)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[0].get(
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

        # Filtramos por origen
        data = {'origen': "Estación 1",
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_reservas_filtros/', headers={
                                    'Authorization': f'Token {token}'}, data=data)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=1, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[1].get("fechaFin"))
        self.assertEqual(self.r1.codigoRecogida, response.data[1].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[1].get(
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
        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=3, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r2.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[0].get(
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

        # Filtramos por usuario
        data = {'usuario': "usuario2",
                }

        # Realiza la petición correctamente
        response = self.client.post('/cibiuam/consultar_reservas_filtros/', headers={
                                    'Authorization': f'Token {token}'}, data=data)

        # Comprueba que las reservas obtenidas son las correctas y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaInicio"))
        self.assertEqual((timezone.localtime()+relativedelta(days=2, minutes=10)
                          ).strftime("%Y-%m-%d %H:%M"), response.data[0].get("fechaFin"))
        self.assertEqual(self.r3.codigoRecogida, response.data[0].get(
            "codigoRecogida"))

        self.assertEqual(0.1, response.data[0].get(
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

        # Crea una nueva estación en zona muy transitada

        data = {'nombre': "Renfe",
                "ubicacion": "Estación Cantoblanco",
                "nAnclajes": 1,
                "latitud": 40.543956612439665,
                "longitud": -3.700142987621462
                }
        # Realiza petición con datos correctos
        response = self.client.post(
            '/cibiuam/alta_estacion/', data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que se haya creado la estación y los anclajes de la estación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Estacion.objects.filter(
            nombre="Renfe").first().ubicacion, "Estación Cantoblanco")
        self.assertEqual(Estacion.objects.filter(
            nombre="Renfe").exists(), True)
        self.assertEqual(response.data.get("Mensaje"),
                         "Estación Renfe creada con éxito.")
        self.assertEqual(Estacion.objects.filter(
            nombre="Renfe").first().anclajes.all().count(), 1)
        self.assertEqual(Anclaje.objects.filter(
            estacion=Estacion.objects.filter(nombre="Renfe").first()).count(), 1)
        self.assertEqual(Anclaje.objects.filter(estacion=Estacion.objects.filter(
            nombre="Renfe").first(), numAnclaje=1).exists(), True)
        self.assertEqual(Anclaje.objects.filter(estacion=Estacion.objects.filter(
            nombre="Renfe").first(), numAnclaje=2).exists(), False)

        # Realiza logout
        response = self.client.post(
            '/auth/token/logout', headers={'Authorization': f'Token {token}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
