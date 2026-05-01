from django.test import TransactionTestCase
from sgu_sgs.models import Estacion, Anclaje, Bicicleta, UsuarioSistema, Contrato, Tarifa, Usuario
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta


class AnclajeModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Calle Madrid", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.est, numAnclaje=2)
        self.est2 = Estacion.objects.create(
            nombre="Prueba2", ubicacion="Calle Sevilla", latitud=2,
            longitud=2.5, nAnclajes=2)
        self.anc3 = Anclaje.objects.create(estacion=self.est2, numAnclaje=1)
        self.anc4 = Anclaje.objects.create(estacion=self.est2, numAnclaje=2)
        self.usuario = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        self.usuario.set_password("contrausuario1")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=179), usuario=self.user, tarifa=self.tarifa)

    def test_001_anclaje_str(self):
        """
        Prueba método str
        """
        self.assertEqual(
            str(self.anc), "Anclaje número 1 de la estación Prueba")

    def test_002_anclaje_anclajeLibre(self):
        """
        Prueba método anclajeLibre
        """
        # Prueba el método para casos en los que no se ancló inicialmente ninguna bicicleta
        bici = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc3)
        # Prueba caso en que no hay reservas previas en ese anclaje
        self.assertEqual(self.anc.anclajeLibre(), True)

        # Si hay reservas anteriores y la última es destino
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=10), fechaFin=timezone.localtime()-relativedelta(minutes=9), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeLibre(), False)

        # Si hay reservas anteriores y la última es origen
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=8), fechaFin=timezone.localtime()-relativedelta(minutes=7), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeLibre(), True)

    def test_003_anclaje_anclajeLibre(self):
        """
        Prueba método anclajeLibre
        """
        # Prueba el método para casos en los que se ancló inicialmente una bicicleta

        # Bicicleta asignada previamente a la asignación de la nueva bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # No hay reservas previas
        bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        bici.fecha = timezone.localtime()-relativedelta(minutes=100)
        bici.save()
        self.assertEqual(self.anc.anclajeLibre(), False)

        # Creamos reservas previas a la asignación de la bicicleta y posterior a la asignación
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=120), fechaFin=timezone.localtime()-relativedelta(minutes=115), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc4, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si hay reservas anteriores y la última es origen
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=75), fechaFin=timezone.localtime()-relativedelta(minutes=70), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.assertEqual(self.anc.anclajeLibre(), True)

        # Si hay reservas anteriores y la última es destino
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=60), fechaFin=timezone.localtime()-relativedelta(minutes=55), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeLibre(), False)

    def test_004_anclaje_anclajeDisponibleAsignacion(self):
        """
        Prueba método anclajeDisponibleAsignacion
        """
        # Prueba el método para casos en los que hay una reserva pendiente de pago en ese anclaje

        # Creamos estación de prueba
        est = Estacion.objects.create(
            nombre="Prueba3", ubicacion="Calle Valencia", latitud=0,
            longitud=0.5, nAnclajes=1)
        anc = Anclaje.objects.create(estacion=est, numAnclaje=1)

        bici = Bicicleta.objects.create(
            estacionInicial=est, anclajeInicio=anc)
        bici.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici.save()
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc4)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reserva pendiente
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=15), importe=0, estado='pendiente',
                                         estOrigen=est, estDestino=self.est2, ancOrigen=anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=20)), False)
        reserva.delete()

        # Creamos reserva pendiente
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=20), importe=0, estado='pendiente',
                               estOrigen=self.est2, estDestino=est, ancOrigen=self.anc4, ancDestino=anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=30)), False)

    def test_005_anclaje_anclajeDisponibleAsignacion(self):
        """
        Prueba método anclajeDisponibleAsignacion
        """
        # Prueba el método para casos en los que no se ancló inicialmente ninguna bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc3)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Prueba caso en que no hay reservas previas en ese anclaje
        # No hay reservas posteriores en las que es destino
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(hours=1)), True)

        # Registramos reserva posterior en la que el anclaje es destino
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=30), fechaFin=timezone.localtime()+relativedelta(minutes=45), importe=0, estado='pagada',
                                         estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=10)), False)
        reserva.delete()

        # Si hay reservas anteriores y la última es destino
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=45), fechaFin=timezone.localtime()-relativedelta(minutes=30), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(hours=1)), False)

        # Si hay reservas anteriores y la última es origen
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=20), fechaFin=timezone.localtime()-relativedelta(minutes=10), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si no hay reservas destino posteriores, está libre
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(hours=1)), True)

        # Creamos reserva en la que es destino después
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada', estOrigen=self.est2,
                               estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=30)), False)

    def test_006_anclaje_anclajeDisponibleAsignacion(self):
        """
        Prueba método anclajeDisponibleAsignacion
        """
        # Prueba el método para casos en los que se ancló inicialmente una bicicleta

        # Bicicleta asignada previamente a la asignación de la nueva bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # No hay reservas previas
        bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)

        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=30)), False)

        # Creamos reservas previas a la asignación de la bicicleta y posterior a la asignación
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=100), fechaFin=timezone.localtime()-relativedelta(minutes=85), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc4, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si hay reservas anteriores y la última es destino
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=5), fechaFin=timezone.localtime()+relativedelta(minutes=10), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=15), fechaFin=timezone.localtime()+relativedelta(minutes=25), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(minutes=45)), False)

        # Si hay reservas anteriores y la última es origen
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=35), fechaFin=timezone.localtime()+relativedelta(minutes=45), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si no hay reservas destino posteriores, está libre
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(hours=1)), True)

        # Creamos reserva en la que es destino después
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=75), fechaFin=timezone.localtime()+relativedelta(minutes=90), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc4, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleAsignacion(
            timezone.localtime()+relativedelta(hours=1)), False)

    def test_007_anclaje_anclajeDisponibleRecogida(self):
        """
        Prueba método anclajeDisponibleRecogida
        """
        # Prueba el método para casos en los que hay una reserva pendiente de pago en ese anclaje

        # Creamos estación de prueba
        est = Estacion.objects.create(
            nombre="Prueba3", ubicacion="Calle Valencia", latitud=0,
            longitud=0.5, nAnclajes=1)
        anc = Anclaje.objects.create(estacion=est, numAnclaje=1)

        bici = Bicicleta.objects.create(
            estacionInicial=est, anclajeInicio=anc)
        bici.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici.save()
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc4)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reserva pendiente
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=15), importe=0, estado='pendiente',
                                         estOrigen=est, estDestino=self.est2, ancOrigen=anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=20)), False)
        reserva.delete()

        # Creamos reserva pendiente
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=10), fechaFin=timezone.localtime()+relativedelta(minutes=20), importe=0, estado='pendiente',
                               estOrigen=self.est2, estDestino=est, ancOrigen=self.anc4, ancDestino=anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=30)), False)

    def test_008_anclaje_anclajeDisponibleRecogida(self):
        """
        Prueba método anclajeDisponibleRecogida
        """
        # Prueba el método para casos en los que no se ancló inicialmente ninguna bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc3)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reserva anterior a fecha deseada
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=45), fechaFin=timezone.localtime()-relativedelta(minutes=30), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Prueba caso en que no hay reservas previas en ese anclaje
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()-relativedelta(minutes=60)), False)

        # Si hay reservas anteriores y la última es destino

        # Si no hay reservas origen posteriores, hay bicicleta para recoger
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(hours=1)), True)

        # Creamos reserva en la que es origen después, no se puede recoger la bicicleta
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=30), fechaFin=timezone.localtime()+relativedelta(hours=1), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=15)), False)
        reserva.delete()

        # Si hay reservas anteriores y la última es origen, no hay bicicleta
        # Creamos reservas
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=25), fechaFin=timezone.localtime()-relativedelta(minutes=10), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(hours=1)), False)

    def test_009_anclaje_anclajeDisponibleRecogida(self):
        """
        Prueba método anclajeDisponibleRecogida
        """
        # Prueba el método para casos en los que se ancló inicialmente una bicicleta

        # Bicicleta asignada previamente a la asignación de la nueva bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reservas previas a la asignación de la bicicleta
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=100), fechaFin=timezone.localtime()-relativedelta(minutes=85), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc4, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)

        # No hay reservas previas ni hay reservas origen después, hay bicicleta
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=30)), True)

        # Creamos reserva origen posterior, no se puede recoger bicicleta
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=5), fechaFin=timezone.localtime()+relativedelta(minutes=10), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=3)), False)

        # Si hay reservas anteriores y la última es origen
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=8)), False)

        # Si hay reservas anteriores y la última es destino
        # Creamos reserva
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=20), fechaFin=timezone.localtime()+relativedelta(minutes=30), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si no hay reservas origen después, se puede recoger bicicleta
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=45)), True)

        # Si hay reservas origen después, no se puede
        # Creamos reserva
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=35), fechaFin=timezone.localtime()+relativedelta(minutes=45), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.anclajeDisponibleRecogida(
            timezone.localtime()+relativedelta(minutes=33)), False)

    def test_010_anclaje_seleccionarBicicleta(self):
        """
        Prueba método seleccionarBicicleta
        """
        # Prueba el método para casos en los que no se ancló inicialmente ninguna bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est2, anclajeInicio=self.anc3)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reserva anterior a fecha deseada
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=45), fechaFin=timezone.localtime()-relativedelta(minutes=30), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Prueba caso en que no hay reservas previas en ese anclaje
        self.assertEqual(self.anc.seleccionarBicicleta(
            timezone.localtime()-relativedelta(minutes=15)), bici2)

    def test_011_anclaje_seleccionarBicicleta(self):
        """
        Prueba método seleccionarBicicleta
        """
        # Prueba el método para casos en los que se ancló inicialmente una bicicleta

        # Bicicleta asignada previamente a la asignación de la nueva bicicleta
        bici2 = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        bici2.fecha = timezone.localtime()-relativedelta(minutes=125)
        bici2.save()

        # Creamos reservas previas a la asignación de la bicicleta
        Reserva.objects.create(fechaInicio=timezone.localtime()-relativedelta(minutes=100), fechaFin=timezone.localtime()-relativedelta(minutes=85), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc4, bicicleta=bici2, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)

        # No hay reservas origen después, bicicleta asignada inicialmente
        self.assertEqual(self.anc.seleccionarBicicleta(
            timezone.localtime()+relativedelta(minutes=30)), bici)

        # Creamos reserva origen y destino posterior a la asignación
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=5), fechaFin=timezone.localtime()+relativedelta(minutes=10), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=20), fechaFin=timezone.localtime()+relativedelta(minutes=30), importe=0, estado='pagada',
                               estOrigen=self.est2, estDestino=self.est, ancOrigen=self.anc3, ancDestino=self.anc, bicicleta=bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.anc.seleccionarBicicleta(
            timezone.localtime()+relativedelta(minutes=40)), bici)
