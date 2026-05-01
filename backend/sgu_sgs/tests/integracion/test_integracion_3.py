from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from sgu_sgs.models import Gestor, UsuarioSistema, Tarifa, Estacion, Anclaje, Bicicleta, Usuario, Contrato
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Intregacion_3_Test(TransactionTestCase):
    """Test de integración 3
        Realiza las acciones cotidianas de un gestor que desea gestionar el servicio:
        - Realiza login
        - Consultar estado de bicicletas y estaciones
        - Dar de alta una estación
        - Dar de alta una bicicleta
        - Consultar contratos
        - Filtrar contratos
        - Actualiza el precio de las tarifas
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
            username="gestor",
            rol="gestor")
        self.usuario.set_password("contragestor")
        self.usuario.save()
        self.gestor = Gestor.objects.create(
            usuario=self.usuario, nombre="luis", apellidos="perez")

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
        self.bici2 = Bicicleta.objects.create(
            estacionInicial=self.e, anclajeInicio=Anclaje.objects.filter(numAnclaje=2, estacion=self.e).first())

        self.usuario2 = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario2.set_password("contrausuario")
        self.usuario2.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario2, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

        self.usuario3 = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        self.usuario3.set_password("contrausuario")
        self.usuario3.save()
        self.user2 = Usuario.objects.create(
            usuario=self.usuario3, nombre="Prueba2", apellidos="Prueba2", saldo=0.0, tlf="111111111")

        self.c = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(
            days=30*6), fin=timezone.localtime().date()-relativedelta(days=1), usuario=self.user, tarifa=self.semestral)
        self.c1 = Contrato.objects.create(inicio=timezone.localtime().date()+relativedelta(
            days=30*6), fin=timezone.localtime().date()+relativedelta(days=30*18 - 1), usuario=self.user2, tarifa=self.anual)

    def test_integracion_3(self):
        # Iniciamos sesión
        data = {'username': "gestor",
                "password": "contragestor"
                }

        # Realiza la petición correctamente con credenciales de un gestor
        response = self.client.post('/auth/token/login', data=data)

        token = response.data.get("auth_token")

        # Consultamos detalles y estado de las estaciones

        data = {'estacion': "EPS"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado/', data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 1)
        self.assertEqual(response.data.get("ocupado"), 1)

        data = {'estacion': "Facultad de Formación de Profesorado y Educación"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado/', data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 2)
        self.assertEqual(response.data.get("ocupado"), 1)

        # Obtener listado y ubicación de estaciones

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

        # Obtener listado con ids de bicicletas del sistema

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/informacion/bicicletas/', headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve todas las bicicletas con su id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("id"), 1)
        self.assertEqual(response.data[1].get("id"), 2)

        # Consultar estado de bicicletas

        data = {'id': 1
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado_bicicleta/',
                                    data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que el estado de la bicicleta es el esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get(
            "Mensaje"), "Bicicleta ubicada en el anclaje número 1 de la estación Facultad de Formación de Profesorado y Educación.")

        # Alta de una bicicleta

        data = {'estacion': "EPS",
                "anclajeId": 1
                }
        # Realiza la petición con datos correctos
        response = self.client.post(
            '/cibiuam/alta_bicicleta/', data=data, headers={'Authorization': f'Token {token}'})

        # Verifica que la bicicleta se haya creado y la respuesta sea la esperada
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bicicleta.objects.filter(
            estacionInicial=self.e, anclajeInicio=Anclaje.objects.filter(numAnclaje=1, estacion=self.e).first()).exists(), True)
        self.assertEqual(response.data.get("Mensaje"),
                         "Bicicleta creada con éxito.")

        # Alta de estación

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

        # Consultamos el estado de la nueva estación

        data = {'estacion': "Renfe"
                }

        # Realiza la petición con los datos correctos
        response = self.client.post('/cibiuam/consultar_estado/', data)

        # Verifica que el estado es el correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("libre"), 1)
        self.assertEqual(response.data.get("ocupado"), 0)

        # Consultamos contratos

        # Realiza la petición correctamente
        response = self.client.get(
            '/cibiuam/consultar_contratos/', headers={'Authorization': f'Token {token}'})

        # Comprueba que los contratos obtenidos son los correctos y existentes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )-relativedelta(days=30*6)), response.data[1].get("inicio"))
        self.assertEqual(
            str(timezone.localtime().date()-relativedelta(days=1)), response.data[1].get("fin"))
        self.assertEqual("semestral", response.data[1].get(
            "tarifa").get("duracion"))

        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date()+relativedelta(
            days=30*6)), response.data[0].get("inicio"))
        self.assertEqual(str(timezone.localtime().date(
        )+relativedelta(days=30*18-1)), response.data[0].get("fin"))
        self.assertEqual("anual", response.data[0].get(
            "tarifa").get("duracion"))

        # Filtra contratos

        # Filtra por tarifa

        data = {"tarifa": "anual"}

        # Realiza la petición con filtros correctos
        response = self.client.post('/cibiuam/consultar_contratos_filtros/',
                                    data=data, headers={'Authorization': f'Token {token}'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )+relativedelta(days=30*6)), response.data[0].get("inicio"))
        self.assertEqual(str(timezone.localtime().date() +
                         relativedelta(days=30*18-1)), response.data[0].get("fin"))
        self.assertEqual("anual", response.data[0].get(
            "tarifa").get("duracion"))

        # Filtra por fecha de inicio

        data = {"inicio": str(timezone.localtime().date())}

        # Realiza la petición con filtros correctos
        response = self.client.post('/cibiuam/consultar_contratos_filtros/',
                                    data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve los contratos que cumplen las condiciones de los filtros
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )+relativedelta(days=30*6)), response.data[0].get("inicio"))
        self.assertEqual(str(timezone.localtime().date() +
                         relativedelta(days=30*18-1)), response.data[0].get("fin"))
        self.assertEqual("anual", response.data[0].get(
            "tarifa").get("duracion"))

        # Filtra por fecha de fin

        data = {"fin": str(timezone.localtime().date())}

        # Realiza la petición con filtros correctos
        response = self.client.post('/cibiuam/consultar_contratos_filtros/',
                                    data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve los contratos que cumplen las condiciones de los filtros
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("usuario", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )-relativedelta(days=30*6)), response.data[0].get("inicio"))
        self.assertEqual(
            str(timezone.localtime().date()-relativedelta(days=1)), response.data[0].get("fin"))
        self.assertEqual("semestral", response.data[0].get(
            "tarifa").get("duracion"))

        # Filtra por fecha de inicio y fin

        data = {"inicio": str(timezone.localtime().date()-relativedelta(days=30*12)),
                "fin": str(timezone.localtime().date()+relativedelta(days=30*2*12))}

        # Realiza la petición con varios filtros a la vez
        response = self.client.post('/cibiuam/consultar_contratos_filtros/',
                                    data=data, headers={'Authorization': f'Token {token}'})

        # Comprueba que devuelve los contratos que cumplen las condiciones de los filtros
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual("usuario", response.data[1].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )-relativedelta(days=30*6)), response.data[1].get("inicio"))
        self.assertEqual(
            str(timezone.localtime().date()-relativedelta(days=1)), response.data[1].get("fin"))
        self.assertEqual("semestral", response.data[1].get(
            "tarifa").get("duracion"))

        self.assertEqual("usuario2", response.data[0].get(
            "usuario").get("usuario").get("username"))
        self.assertEqual(str(timezone.localtime().date(
        )+relativedelta(days=30*6)), response.data[0].get("inicio"))
        self.assertEqual(str(timezone.localtime().date() +
                         relativedelta(days=30*18-1)), response.data[0].get("fin"))
        self.assertEqual("anual", response.data[0].get(
            "tarifa").get("duracion"))

        # Actualiza importe de la tarifa mensual

        data = {'nombre': "mensual",
                "importe": 20
                }
        # Realiza la petición con datos correctos
        response = self.client.post(
            '/cibiuam/actualizar_tarifa/', data=data, headers={'Authorization': f'Token {token}'})

        # Verifica que la tarifa tenga el nuevo importe
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tarifa.objects.filter(
            duracion="mensual").first().importe, 20)
        self.assertEqual(response.data.get("Mensaje"),
                         "Tarifa actualizada con éxito.")

        # Actualiza importe y precio por minuto tarifa semestral

        data = {'nombre': "semestral",
                "importe": 2,
                "precioMinuto": 2
                }
        # Realiza la petición con datos correctos
        response = self.client.post(
            '/cibiuam/actualizar_tarifa/', data=data, headers={'Authorization': f'Token {token}'})

        # Verifica que la tarifa tenga el nuevo precio por minuto e importe
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tarifa.objects.filter(
            duracion="semestral").first().importe, 2)
        self.assertEqual(Tarifa.objects.filter(
            duracion="semestral").first().importe, 2)
        self.assertEqual(response.data.get("Mensaje"),
                         "Tarifa actualizada con éxito.")

        # Realiza logout
        response = self.client.post(
            '/auth/token/logout', headers={'Authorization': f'Token {token}'})

        # Verifica que logout es correcto
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
