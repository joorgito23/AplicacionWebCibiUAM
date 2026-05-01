from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Usuario, Tarifa, Contrato, Notificacion, Estacion, Anclaje, Bicicleta
from sgr.models import Reserva
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class UsuarioModelTest(TransactionTestCase):
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

    def test_001_usuario_str(self):
        """"
        Prueba método str
        """
        self.assertEqual(
            str(self.user), "usuario (usuario) - Prueba Prueba, 111111111. Saldo: 0.0")

    def test_002_usuario_getPerfil(self):
        """
        Prueba método getPerfil
        """

        # Verifica que los datos coinciden con los del usuario
        data = self.user.getPerfil()
        self.assertEqual(data["usuario"], "usuario")
        self.assertEqual(data["nombre"], "Prueba")
        self.assertEqual(data["apellidos"], "Prueba")
        self.assertEqual(data["rol"], "usuario")
        self.assertEqual(data["duracion"], "Mensual")
        self.assertEqual(
            data["fin"], timezone.localtime().date()+relativedelta(days=29))
        self.assertEqual(data["saldo"], 0.0)
        self.assertEqual(data["tlf"], "111111111")

        usuario2 = UsuarioSistema(
            username="usuario2",
            rol="usuario")
        usuario2.set_password("contrausuario")
        usuario2.save()
        user2 = Usuario.objects.create(
            usuario=usuario2, nombre="Prueba2", apellidos="Prueba", saldo=0.0, tlf="111111111")
        Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(
            days=30*2), fin=timezone.localtime().date()-relativedelta(days=30*2)+relativedelta(days=29), usuario=user2, tarifa=self.tarifa)

        # Verifica que si el usuario no tiene contrato muestra dicha información correctamente
        data = user2.getPerfil()
        self.assertEqual(data["usuario"], "usuario2")
        self.assertEqual(data["nombre"], "Prueba2")
        self.assertEqual(data["apellidos"], "Prueba")
        self.assertEqual(data["rol"], "usuario")
        self.assertEqual(data["duracion"], "Sin tarifa contratada actualmente")
        self.assertEqual(data["fin"], "Sin tarifa contratada actualmente")
        self.assertEqual(data["saldo"], 0.0)
        self.assertEqual(data["tlf"], "111111111")

    def test_003_usuario_verificarTlf(self):
        """
        Prueba método verificarTlf
        """
        # Prueba que el método valida teléfonos correctos e incorrectos
        self.assertEqual(self.user.verificarTlf("11"), False)
        self.assertEqual(self.user.verificarTlf("11111111g"), False)
        self.assertEqual(self.user.verificarTlf("111111111"), True)

    def test_004_usuario_modificarPerfil(self):
        """
        Prueba método modificarPerfil
        """

        # Comprueba que el método actualiza el perfil correctamente
        self.assertEqual(self.user.modificarPerfil("222222222"), True)
        self.assertEqual(Usuario.objects.filter(
            nombre="Prueba").first().tlf, "222222222")
        self.assertEqual(self.user.modificarPerfil("error"), False)

    def test_005_usuario_getContratoActual(self):
        """Prueba método getContratoActual
        """

        # Prueba que el método devuelva el contrato actual
        self.assertEqual(self.user.getContratoActual(), self.c)

    def test_006_usuario_calcularFechaFinContrato(self):
        """
        Pruena método calcularFechaFinContrato
        """

        # Comprueba que el método calcula la fecha fin de un contrato a partir de una tarifa y fehca de inicio
        self.assertEqual(self.user.calcularFechaFinContrato(timezone.localtime(
        ).date(), self.tarifa), timezone.localtime().date()+relativedelta(days=29))
        t2 = Tarifa.objects.create(
            importe=5, precioMinuto=1, descripcion="Prueba", duracion="semestral")
        self.assertEqual(self.user.calcularFechaFinContrato(
            timezone.localtime().date(), t2), timezone.localtime().date()+relativedelta(days=30*6-1))
        t3 = Tarifa.objects.create(
            importe=8, precioMinuto=1, descripcion="Prueba", duracion="anual")
        self.assertEqual(self.user.calcularFechaFinContrato(
            timezone.localtime().date(), t3), timezone.localtime().date()+relativedelta(days=30*12-1))

    def test_007_usuario_crearContrato(self):
        """
        Prueba método crearContrato
        """

        # Crea un usuario sin contrato
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")

        # Crea un nuevo contrato al usuario y verifica que existe
        user1.crearContrato(self.tarifa)
        self.assertEqual(Contrato.objects.filter(usuario=user1, inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), tarifa=self.tarifa).first(), user1.contratos.all().first())

    def test_008_usuario_getFechaInicioContrato(self):
        """
        Prueba método getFechaInicioContrato
        """

        # Crea un usuario para comprobar que el método calcula bien la fecha de inicio del contrato
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        # Usuario sin contrato
        self.assertEqual(user1.getFechaInicioContrato(),
                         timezone.localtime().date())

        # Usuario con contrato
        user1.crearContrato(self.tarifa)
        self.assertEqual(user1.getFechaInicioContrato(), timezone.localtime(
        ).date() + relativedelta(days=30))

    def test_009_usuario_getFechaInicioContrato(self):
        """
        Prueba método getFechaInicioContrato
        """

        # Comprobar que el método calcula bien la fecha de inicio del contrato para el caso de un contrato caducado
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        Contrato.objects.create(inicio=timezone.localtime().date() - relativedelta(days=30*2),
                                fin=timezone.localtime().date() - relativedelta(days=30*2) + relativedelta(days=29), usuario=user1, tarifa=self.tarifa)
        self.assertEqual(user1.getFechaInicioContrato(),
                         timezone.localtime().date())

    def test_010_usuario_renovarContrato(self):
        """
        Prueba método renovarContrato
        """

        # Prueba la renovación del contrato verificando que las fechas son correctas

        # Crea usuario
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")

        # Crea contrato inicial
        user1.crearContrato(self.tarifa)

        # Renueva contrato
        user1.renovarContrato(self.tarifa)

        # Verifica que el contrato creado tiene las fechas correctas
        contrato = Contrato.objects.filter(
            usuario=user1).order_by("-fin").first()
        self.assertEqual(contrato.inicio, timezone.localtime().date() +
                         relativedelta(days=30))
        self.assertEqual(contrato.fin, timezone.localtime().date(
        ) + relativedelta(days=30) + relativedelta(days=29))

    def test_011_usuario_avisarExpiracionContrato(self):
        """
        Prueba método avisarExpiracionContrato
        """
        # Comprueba que el sistema crea una notificación para avisar de la expiración del contrato
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        c1 = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=user1, tarifa=self.tarifa)
        self.assertEqual(user1.avisarExpiracionContrato(), True)
        self.assertEqual(Notificacion.objects.filter(fecha=c1.getFin() - relativedelta(days=10), usuario=user1,
                         msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").exists(), True)

    def test_012_usuario_avisarExpiracionContrato(self):
        """
        Prueba método avisarExpiracionContrato
        """

        # Comprueba que el sistema no debe avisar al usuario al no tener contrato activo
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.assertEqual(user1.avisarExpiracionContrato(), False)
        self.assertEqual(Notificacion.objects.filter(
            usuario=user1, msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").exists(), False)

    def test_013_usuario_avisarExpiracionContrato(self):
        """
        Prueba método avisarExpiracionContrato
        """

        # Comprueba que el sistema no debe avisar al usuario dado que quedan más de 10 días de contrato
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=29), usuario=user1, tarifa=self.tarifa)
        self.assertEqual(user1.avisarExpiracionContrato(), False)
        self.assertEqual(Notificacion.objects.filter(
            usuario=user1, msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").exists(), False)

    def test_014_usuario_avisarExpiracionContrato(self):
        """
        Prueba método avisarExpiracionContrato
        """

        # Verifica que envía la notificación al quedar menos de 10 días de contrato
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        c1 = Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
        ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=user1, tarifa=self.tarifa)
        self.assertEqual(user1.avisarExpiracionContrato(), True)
        self.assertEqual(Notificacion.objects.filter(fecha=c1.getFin() - relativedelta(days=10), usuario=user1,
                         msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").count(), 1)

        # Al volver a intentarlo no lo envía porque ya se ha generado la notificación
        self.assertEqual(user1.avisarExpiracionContrato(), False)
        self.assertEqual(Notificacion.objects.filter(fecha=c1.getFin() - relativedelta(days=10), usuario=user1,
                         msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").count(), 1)

    def test_015_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Reserva no posible con fecha inicio posterior a fin
        self.assertEqual(self.user.reservaPosible(
            timezone.localtime()+relativedelta(hours=1), timezone.localtime()), False)

    def test_016_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Creamos un usuario sin contrato y comprobamos que no permite reserva
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.assertEqual(user1.reservaPosible(timezone.localtime(
        )+relativedelta(hours=1), timezone.localtime()+relativedelta(hours=2)), False)

    def test_017_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Reserva no posible debido a que la fecha de inicio es anterior al fin de otra reserva
        Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2, hours=1), fechaFin=timezone.localtime()+relativedelta(days=4, hours=2), importe=0, estado='pagada',
                               estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.user.reservaPosible(timezone.localtime()+relativedelta(days=3,
                         hours=1, minutes=30), timezone.localtime()+relativedelta(days=5, hours=3)), False)

    def test_018_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Reserva no posible debido a que la fecha de fin es posterior al inicio de otra reserva
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2, hours=1), fechaFin=timezone.localtime()+relativedelta(days=4, hours=2), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.user.reservaPosible(timezone.localtime()+relativedelta(days=1,
                         hours=1, minutes=30), timezone.localtime()+relativedelta(days=3, hours=30)), False)
        reserva.delete()

    def test_019_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Reserva no posible puesto que misma fecha pero horas no compatibles
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(days=2, hours=1), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.user.reservaPosible(timezone.localtime(
        )+relativedelta(days=2), timezone.localtime()+relativedelta(days=3, hours=3)), False)
        reserva.delete()

        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2, hours=1), fechaFin=timezone.localtime()+relativedelta(days=3, hours=2), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.user.reservaPosible(timezone.localtime()+relativedelta(
            days=1, hours=2), timezone.localtime()+relativedelta(days=2, hours=3)), False)
        reserva.delete()

    def test_020_usuario_reservaPosible(self):
        """
        Prueba método reservaPosible
        """

        # Verifica que permite la reserva con condiciones válidas pues no dispone de ninguna reserva previa
        self.assertEqual(self.user.reservaPosible(timezone.localtime()+relativedelta(
            days=1, hours=2), timezone.localtime()+relativedelta(days=2, hours=3)), True)

    def test_021_usuario_calcularPrecioReservaUsuario(self):
        """
        Prueba método calcularPrecioReservaUsuario
        """

        # Error debido a fecha de inicio posterior a fin
        self.assertEqual(self.user.calcularPrecioReservaUsuario(
            timezone.localtime()+relativedelta(hours=1), timezone.localtime()), -1)

    def test_022_usuario_calcularPrecioReservaUsuario(self):
        """
        Prueba método calcularPrecioReservaUsuario
        """

        # Creamos un usuario sin contrato y comprobamos que no calcula importe
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        self.assertEqual(user1.calcularPrecioReservaUsuario(timezone.localtime(
        )+relativedelta(hours=1), timezone.localtime()+relativedelta(hours=2)), -1)

    def test_023_usuario_calcularPrecioReservaUsuario(self):
        """
        Prueba método calcularPrecioReservaUsuario
        """

        # Creamos contrato semestral y calculamos precio correctamente
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=0.0, tlf="111111111")
        tarifa2 = Tarifa.objects.create(
            importe=5, precioMinuto=0.01, descripcion="Prueba", duracion="semestral")
        Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
        ).date()+relativedelta(days=179), usuario=user1, tarifa=tarifa2)
        self.assertEqual(user1.calcularPrecioReservaUsuario(timezone.localtime(
        )+relativedelta(hours=1), timezone.localtime()+relativedelta(hours=2)), 0.6)

    def test_024_usuario_precioReservaSaldo(self):
        """
        Prueba método precioReservaSaldo
        """

        # Creamos usuario con saldo
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=5.0, tlf="111111111")

        # Comprobamos cálculo correcto del importe final
        self.assertEqual(user1.precioReservaSaldo(12), 7)
        self.assertEqual(user1.precioReservaSaldo(3), 0)
        self.assertEqual(user1.precioReservaSaldo(-2), -1)

    def test_025_usuario_actualizarSaldo(self):
        """
        Prueba método actualizarSaldo
        """

        # Creamos usuario con saldo
        usuario1 = UsuarioSistema(
            username="usuario1",
            rol="usuario")
        usuario1.set_password("contrausuario1")
        usuario1.save()
        user1 = Usuario.objects.create(
            usuario=usuario1, nombre="Prueba1", apellidos="Prueba1", saldo=3.0, tlf="111111111")

        # Comprobamos que actualiza el saldo dado un importe correctamente
        self.assertEqual(user1.actualizarSaldo(2), True)
        self.assertEqual(Usuario.objects.filter(
            nombre="Prueba1").first().saldo, 5)
        self.assertEqual(user1.actualizarSaldo(-3), True)
        self.assertEqual(Usuario.objects.filter(
            nombre="Prueba1").first().saldo, 2)
        self.assertEqual(user1.actualizarSaldo(-3), True)
        self.assertEqual(Usuario.objects.filter(
            nombre="Prueba1").first().saldo, 0)

    def test_026_usuario_getReservaById(self):
        """
        Prueba método getReservaById
        """

        # Creamos una reserva y la buscamos por su id
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(days=2, hours=2), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        self.assertEqual(self.user.getReservaById(reserva.id), reserva)

        # Reserva no existente
        self.assertEqual(self.user.getReservaById(8), None)

    def test_027_usuario_getReservas(self):
        """
        Prueba método getReservas
        """

        # Creamos reservas para obtenerlas
        reserva = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada',
                                         estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        reserva2 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=1), fechaFin=timezone.localtime()+relativedelta(hours=2), importe=0, estado='pagada',
                                          estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        reserva3 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=5), fechaFin=timezone.localtime()+relativedelta(hours=6), importe=0, estado='pagada',
                                          estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        reserva4 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(hours=7), fechaFin=timezone.localtime()+relativedelta(hours=8), importe=0, estado='pagada',
                                          estOrigen=self.est, estDestino=self.est2, ancOrigen=self.anc, ancDestino=self.anc3, bicicleta=self.bici, usuario=self.user, expires_at=timezone.localtime() + timedelta(minutes=10))
        reservas = self.user.getReservas()
        self.assertEqual(reservas.count(), 4)
        self.assertIn(reserva, reservas)
        self.assertIn(reserva2, reservas)
        self.assertIn(reserva3, reservas)
        self.assertIn(reserva4, reservas)
