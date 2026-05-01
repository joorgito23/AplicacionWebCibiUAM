from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Usuario, Tarifa, Contrato, Notificacion, Estacion, Anclaje, Bicicleta
from sgr.models import Reserva
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class ReservaModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        self.usuario.set_password("contrausuario")
        self.usuario.save()
        self.user = Usuario.objects.create(
            usuario=self.usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")
        self.tarifa = Tarifa.objects.create(
            importe=10, precioMinuto=0, descripcion="Prueba", duracion="mensual")
        self.c = Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=self.user, tarifa=self.tarifa)

        self.est = Estacion.objects.create(
            nombre="Prueba", ubicacion="Prueba", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc = Anclaje.objects.create(estacion=self.est, numAnclaje=1)
        self.anc2 = Anclaje.objects.create(estacion=self.est, numAnclaje=2)
        self.bici = Bicicleta.objects.create(
            estacionInicial=self.est, anclajeInicio=self.anc)
        self.est2 = Estacion.objects.create(
            nombre="Prueba2", ubicacion="Prueba2", latitud=0,
            longitud=0.5, nAnclajes=2)
        self.anc3 = Anclaje.objects.create(estacion=self.est2, numAnclaje=1)
        self.anc4 = Anclaje.objects.create(estacion=self.est2, numAnclaje=2)

    def test_001_reserva_str(self):
        """"
        Prueba método str
        """
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))

        self.assertEqual(
            str(r), f"Inicio: {r.fechaInicio.strftime("%Y-%m-%d %H:%M")} - Fin: {r.fechaFin.strftime("%Y-%m-%d %H:%M")} - Codigo: {r.codigoRecogida} - Importe: {r.importe}€ - Estado: {r.estado} - Estación de origen: {r.estOrigen.nombre}, anclaje número {r.ancOrigen.numAnclaje} - Estación de destino: {r.estDestino.nombre}, anclaje número {r.ancDestino.numAnclaje} - Usuario: {r.usuario.usuario.username}"
        )

    def test_002_reserva_notificarReserva(self):
        """"
        Prueba método notificarReserva
        """

        # Crea una reserva y notifica al usuario
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        r.notificarReserva()
        self.assertEqual(Notificacion.objects.filter(
            usuario=self.user, msg=f"A continuación se indica un resumen de su reserva. Inicio: {timezone.localtime(r.fechaInicio).strftime("%Y-%m-%d %H:%M")} - Fin: {timezone.localtime(r.fechaFin).strftime("%Y-%m-%d %H:%M")}. Origen: {r.estOrigen.nombre} nº {r.ancOrigen.numAnclaje} - Destino: {r.estDestino.nombre} nº {r.ancDestino.numAnclaje}. Código de recogida: {r.codigoRecogida}").exists(), True)

    def test_003_reserva_esCancelable(self):
        """"
        Prueba método esCancelable
        """

        # Reserva cancelable
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=2), fechaFin=timezone.localtime()+relativedelta(hours=3), importe=0, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(r.esCancelable(), True)

        r.delete()

        # Reserva no cancelable
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=30), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(r.esCancelable(), False)

    def test_004_reserva_actualizarEstado(self):
        """"
        Prueba método actualizarEstado
        """

        # Crea una reserva y actualiza su estado a cancelada
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=2), fechaFin=timezone.localtime()+relativedelta(hours=3), importe=0, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        r.actualizarEstado('cancelada')
        self.assertEqual(r.estado, 'cancelada')

    def test_005_reserva_devolverImporte(self):
        """"
        Prueba método devolverImporte
        """

        # Crea una reserva y devuelve el importe al usuario
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=2), fechaFin=timezone.localtime()+relativedelta(hours=3), importe=5.75, estado='pagada', estOrigen=self.est,
                                   estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        r.devolverImporte()
        self.assertEqual(self.user.saldo, 5.75)

    def test_006_reserva_cancelar(self):
        """"
        Prueba método cancelar
        """

        # Crea la reserva y la cancela verificando que actualiza el estado y el saldo del usuario
        r = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1, minutes=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=5.75, estado='pagada',
                                   estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        r.cancelar()
        self.assertEqual(self.user.saldo, 5.75)
        self.assertEqual(r.estado, 'cancelada')
