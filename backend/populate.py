import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from datetime import timedelta
from django.utils import timezone
from sgr.models import Reserva
from sgu_sgs.models import Administrador, UsuarioSistema, Tarifa, Usuario, Estacion, Anclaje, Bicicleta, Notificacion, Contrato, Gestor
from dateutil.relativedelta import relativedelta


def populate():

    # Tarifas del sistema

    # Mensual
    # Esta tarifa permite realizar un número de reservas ilimitadas a coste 0. Durante los 30 días del contrato podrá hacer un uso intensivo del servicio sin ningun coste adicional por reserva. No dejes escapar esta tarifa y descubre los beneficios de CibiUAM.
    mensual = Tarifa.objects.create(
        importe=10, precioMinuto=0, descripcion="Disfruta de la máxima tranquilidad con una cuota fija al mes. Con esta tarifa puedes reservar una bicicleta siempre que quieras sin pagar un importe extra por cada uso. Ideal si utilizas el servicio con frecuencia y quieres olvidarte de costes adicionales para cada reserva realizada.", duracion="mensual")

    # Semestral
    # Esta tarifa permite acceder al servicio con un coste menor que la tarifa mensual. Además, podrás realizar reservas con un precio por minuto muy asequible para desplazarte por el campus de la UAM.
    semestral = Tarifa.objects.create(
        importe=5, precioMinuto=0.01, descripcion="Ahorra con una cuota fija más baja y paga únicamente por el tiempo que realmente utilices. Es la opción perfecta si utilizas la bicicleta de manera ocasional, ya que te permite disfrutar de una suscripción más económica y flexible a medio plazo, adaptándose a tus necesidades sin comprometer tu libertad de uso.", duracion="semestral")

    # Anual
    # Esta tarifa permite hacer uso del servicio durante un año completo sin necesidad de preocuparte por la expiración de tu contrato. Además, está pensada para usuarios que no hacen un uso exhaustivo del servicio ofreciendo un precio asequible por minuto para realizar desplazamientos en bicicleta cuando lo desee.
    anual = Tarifa.objects.create(importe=8, precioMinuto=0.01,
                                  descripcion="Esta es la tarifa más económica para usuarios habituales a largo plazo. Cuenta con una cuota fija baja y un pequeño coste por minuto en cada reserva, permitiéndote disfrutar del servicio todo el año con el mejor equilibrio entre ahorro y flexibilidad.", duracion="anual")

    # Usuarios del sistema

    # Administrador
    usuarioSistema = UsuarioSistema(username="admin", rol="administrador")
    usuarioSistema.set_password("Contraadmin-26")
    usuarioSistema.save()
    Administrador.objects.create(usuario=usuarioSistema)

    # Usuarios
    usuarioSistema2 = UsuarioSistema(username="joseRF", rol="usuario")
    usuarioSistema2.set_password("Contrausuario-26")
    usuarioSistema2.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema2, nombre="José", apellidos="Rodríguez Fernández", tlf="658357475", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=30*12),
                            fin=timezone.localtime().date()-relativedelta(days=1), usuario=usuario, tarifa=anual)
    usuario.crearContrato(mensual)
    Notificacion.objects.create(
        fecha=timezone.localtime().date(), msg="A lo largo del día de hoy, se van a realizar actividades de mantenimiento y actualización de la aplicación pudiendo experimentar desconexiones temporales en la aplicación. En dicho caso, acceda de nuevo a la aplicación. Disculpen las molestias.", usuario=usuario)
    Notificacion.objects.create(
        fecha=timezone.localtime().date(), msg="¿Estás disfrutando del servicio? Ponte en contacto con nosotros para darnos tu opinión y mejorar la aplicación con las sugerencias de los usuarios.", usuario=usuario)
    Notificacion.objects.create(fecha=timezone.localtime().date(
    )-relativedelta(days=30*12), msg="Recientemente los gestores del servicio han incorporado nuevas estaciones al campus de la UAM para mejorar la experiencia del usuario. Obtenga más información en la sección correspondiente.", usuario=usuario)

    usuarioSistema3 = UsuarioSistema(
        username="luisGG", rol="usuario")
    usuarioSistema3.set_password("Contrausuario-26")
    usuarioSistema3.save()
    usuario2 = Usuario.objects.create(
        usuario=usuarioSistema3, nombre="Luis", apellidos="González González", tlf="639056263", saldo=0.0)
    Notificacion.objects.create(
        fecha=timezone.localtime().date(), msg="¿Estás disfrutando del servicio? Ponte en contacto con nosotros para darnos tu opinión y mejorar la aplicación con las sugerencias de los usuarios.", usuario=usuario2)
    Notificacion.objects.create(
        fecha=timezone.localtime().date(), msg="Se espera una actualización del servicio a lo largo del día de hoy. Podría experimentar desconexiones temporales a la aplicación. En dicho caso, acceda de nuevo a la aplicación. Disculpen las molestias.", usuario=usuario2)
    Notificacion.objects.create(fecha=timezone.localtime().date(
    )-relativedelta(days=30*12), msg="Recientemente los gestores del servicio han incorporado nuevas estaciones al campus de la UAM para mejorar la experiencia del usuario. Obtenga más información en la sección correspondiente.", usuario=usuario2)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=30*6),
                            fin=timezone.localtime().date()-relativedelta(days=1), usuario=usuario2, tarifa=semestral)
    Contrato.objects.create(inicio=timezone.localtime().date(),
                            fin=timezone.localtime().date()+relativedelta(days=30*12-1), usuario=usuario2, tarifa=anual)

    # Gestores
    usuarioSistema4 = UsuarioSistema(username="m.perez", rol="gestor")
    usuarioSistema4.set_password("Contragestor-26")
    usuarioSistema4.save()
    Gestor.objects.create(
        usuario=usuarioSistema4, nombre="María", apellidos="Pérez Gómez")
    usuarioSistema5 = UsuarioSistema(username="j.ortega", rol="gestor")
    usuarioSistema5.set_password("Contragestor-26")
    usuarioSistema5.save()
    Gestor.objects.create(
        usuario=usuarioSistema5, nombre="Juan", apellidos="Ortega García")
    usuarioSistema6 = UsuarioSistema(username="i.lopez", rol="gestor")
    usuarioSistema6.set_password("Contragestor-26")
    usuarioSistema6.save()
    Gestor.objects.create(
        usuario=usuarioSistema6, nombre="Isabel", apellidos="López Sánchez")
    usuarioSistema7 = UsuarioSistema(username="i.martin", rol="gestor")
    usuarioSistema7.set_password("Contragestor-26")
    usuarioSistema7.save()
    Gestor.objects.create(
        usuario=usuarioSistema7, nombre="Iván", apellidos="Martín Martín")
    usuarioSistema8 = UsuarioSistema(username="p.hernandez", rol="gestor")
    usuarioSistema8.set_password("Contragestor-26")
    usuarioSistema8.save()
    Gestor.objects.create(
        usuario=usuarioSistema8, nombre="Pilar", apellidos="Hernández Gómez")

    # Más usuarios
    usuarioSistema9 = UsuarioSistema(username="jorge23", rol="usuario")
    usuarioSistema9.set_password("Contrausuario-26")
    usuarioSistema9.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema9, nombre="Jorge", apellidos="López Sánchez", tlf="652564750", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=30*2), fin=timezone.localtime(
    ).date()-relativedelta(days=30*2)+relativedelta(days=30*12 - 1), usuario=usuario, tarifa=anual)
    usuario.renovarContrato(mensual)

    usuarioSistema9 = UsuarioSistema(username="diego_27", rol="usuario")
    usuarioSistema9.set_password("Contrausuario-26")
    usuarioSistema9.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema9, nombre="Diego", apellidos="García García", tlf="658347200", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=12), fin=timezone.localtime(
    ).date()-relativedelta(days=12)+relativedelta(days=29), usuario=usuario, tarifa=mensual)
    usuario.renovarContrato(anual)

    usuarioSistema9 = UsuarioSistema(username="alvaro_99", rol="usuario")
    usuarioSistema9.set_password("Contrausuario-26")
    usuarioSistema9.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema9, nombre="Álvaro", apellidos="Martínez Sánchez", tlf="754879080", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=22), fin=timezone.localtime(
    ).date()-relativedelta(days=22)+relativedelta(days=30*6 - 1), usuario=usuario, tarifa=semestral)
    usuario.renovarContrato(mensual)

    usuarioSistema9 = UsuarioSistema(
        username="raul_lopezSanchez", rol="usuario")
    usuarioSistema9.set_password("Contrausuario-26")
    usuarioSistema9.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema9, nombre="Raúl", apellidos="López Sánchez", tlf="784747457", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=28), fin=timezone.localtime(
    ).date()-relativedelta(days=28)+relativedelta(days=29), usuario=usuario, tarifa=mensual)
    usuario.renovarContrato(mensual)

    usuarioSistema9 = UsuarioSistema(username="sgs_1970", rol="usuario")
    usuarioSistema9.set_password("Contrausuario-26")
    usuarioSistema9.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema9, nombre="Sonia", apellidos="Gómez Sánchez", tlf="777945675", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=30*11 + 22), fin=timezone.localtime(
    ).date()-relativedelta(days=30*11 + 22)+relativedelta(days=30*12 - 1), usuario=usuario, tarifa=anual)

    # Estaciones
    e = Estacion.objects.create(
        nombre="EPS", ubicacion="C. Francisco Tomás y Valiente, 11, Fuencarral, 28049 Madrid", latitud=40.546889866859786,
        longitud=-3.6914786766332512, nAnclajes=6)
    e.crearAnclajes()
    e1 = Estacion.objects.create(
        nombre="Facultad de Formación de Profesorado y Educación", ubicacion="C. Francisco Tomás y Valiente, 3, Fuencarral, 28049 Madrid", latitud=40.54436792177776,
        longitud=-3.6979016357348478, nAnclajes=6)
    e1.crearAnclajes()
    e2 = Estacion.objects.create(
        nombre="Renfe", ubicacion="Estación de Cantoblanco", latitud=40.54379767764618,
        longitud=-3.699826939221272, nAnclajes=8)
    e2.crearAnclajes()
    e3 = Estacion.objects.create(
        nombre="Facultad de Ciencias", ubicacion="C. Francisco Tomás y Valiente, 7, Fuencarral, 28049 Madrid", latitud=40.54526750576296,
        longitud=-3.69531385121391, nAnclajes=6)
    e3.crearAnclajes()
    e4 = Estacion.objects.create(
        nombre="Facultad de Psicología", ubicacion="C. Iván Pavlov, 6, Fuencarral, 28049 Madrid", latitud=40.543964522051944,
        longitud=-3.6923935051812315, nAnclajes=6)
    e4.crearAnclajes()
    e5 = Estacion.objects.create(
        nombre="Facultad de Derecho", ubicacion="C. Kelsen, 1, Fuencarral, 28049 Madrid", latitud=40.54148919674131,
        longitud=-3.691187037341344, nAnclajes=6)
    e5.crearAnclajes()
    e6 = Estacion.objects.create(
        nombre="Residencia de Estudiantes", ubicacion="C. de Erasmo de Rotterdam, 5-7, Fuencarral, 28049 Madrid", latitud=40.54815120732193,
        longitud=-3.698854796706824, nAnclajes=6)
    e6.crearAnclajes()
    e7 = Estacion.objects.create(
        nombre="Ctra.M607-Univ.Autónoma", ubicacion="Fuencarral, 28049 Madrid", latitud=40.54075768621728,
        longitud=-3.6969691425355142, nAnclajes=8)
    e7.crearAnclajes()
    e8 = Estacion.objects.create(
        nombre="Polideportivo UAM", ubicacion="Calle Freud, 11, Fuencarral, 28049 Madrid", latitud=40.54590088057905,
        longitud=-3.7006243532976386, nAnclajes=6)
    e8.crearAnclajes()

    # Bicicletas
    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e.getAnclajeByNumAnclaje(i+1), estacionInicial=e)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e1.getAnclajeByNumAnclaje(i+1), estacionInicial=e1)

    for i in range(6):
        Bicicleta.objects.create(
            anclajeInicio=e2.getAnclajeByNumAnclaje(i+1), estacionInicial=e2)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e3.getAnclajeByNumAnclaje(i+1), estacionInicial=e3)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e4.getAnclajeByNumAnclaje(i+1), estacionInicial=e4)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e5.getAnclajeByNumAnclaje(i+1), estacionInicial=e5)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e6.getAnclajeByNumAnclaje(i+1), estacionInicial=e6)

    for i in range(6):
        Bicicleta.objects.create(
            anclajeInicio=e7.getAnclajeByNumAnclaje(i+1), estacionInicial=e7)

    for i in range(4):
        Bicicleta.objects.create(
            anclajeInicio=e8.getAnclajeByNumAnclaje(i+1), estacionInicial=e8)

    # Reservas
    r3 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=3, hours=1), fechaFin=timezone.localtime()+relativedelta(days=3, hours=1, minutes=15), importe=0.2, estado='pagada',
                                estOrigen=e7, estDestino=e8, ancOrigen=Anclaje.objects.filter(
        estacion=e7, numAnclaje=1).first(), ancDestino=Anclaje.objects.filter(
        estacion=e8, numAnclaje=5).first(), bicicleta=Bicicleta.objects.filter(anclajeInicio=e7.getAnclajeByNumAnclaje(1)).first(), usuario=usuario2, expires_at=timezone.localtime() + timedelta(minutes=10))
    r3.notificarReserva()
    r4 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=1, minutes=20), fechaFin=timezone.localtime()+relativedelta(days=1, minutes=30), importe=0, estado='pagada',
                                estOrigen=e8, estDestino=e7, ancOrigen=Anclaje.objects.filter(
        estacion=e8, numAnclaje=1).first(), ancDestino=Anclaje.objects.filter(
        estacion=e7, numAnclaje=7).first(), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=usuario2, expires_at=timezone.localtime() + timedelta(minutes=10))
    r4.notificarReserva()
    r4.actualizarEstado('cancelada')

    # Pruebas reservas de sgs_1970
    r2 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=5), fechaFin=timezone.localtime()+relativedelta(minutes=10), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(minutes=5), timezone.localtime()+relativedelta(minutes=10)), estado='pagada',
                                estOrigen=e2, estDestino=e, ancOrigen=Anclaje.objects.filter(
        estacion=e2, numAnclaje=2).first(), ancDestino=Anclaje.objects.filter(
        estacion=e, numAnclaje=6).first(), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(2)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r2.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=70), fechaFin=timezone.localtime()+relativedelta(minutes=80), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(minutes=70), timezone.localtime()+relativedelta(minutes=80)), estado='pagada',
                                estOrigen=e3, estDestino=e4, ancOrigen=e3.getAnclajeByNumAnclaje(1), ancDestino=e4.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e3.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=200), fechaFin=timezone.localtime()+relativedelta(minutes=210), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(minutes=200), timezone.localtime()+relativedelta(minutes=210)), estado='pagada',
                                estOrigen=e4, estDestino=e3, ancOrigen=e4.getAnclajeByNumAnclaje(5), ancDestino=e3.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e3.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=1, minutes=30), fechaFin=timezone.localtime()+relativedelta(days=1, minutes=40), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=1, minutes=30), timezone.localtime()+relativedelta(days=1, minutes=40)), estado='pagada',
                                estOrigen=e2, estDestino=e, ancOrigen=e2.getAnclajeByNumAnclaje(1), ancDestino=e.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=1, minutes=220), fechaFin=timezone.localtime()+relativedelta(days=1, minutes=230), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=1, minutes=220), timezone.localtime()+relativedelta(days=1, minutes=230)), estado='pagada',
                                estOrigen=e, estDestino=e2, ancOrigen=e.getAnclajeByNumAnclaje(5), ancDestino=e2.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2, minutes=30), fechaFin=timezone.localtime()+relativedelta(days=2, minutes=40), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=2, minutes=30), timezone.localtime()+relativedelta(days=2, minutes=40)), estado='pagada',
                                estOrigen=e2, estDestino=e, ancOrigen=e2.getAnclajeByNumAnclaje(1), ancDestino=e.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2, minutes=220), fechaFin=timezone.localtime()+relativedelta(days=2, minutes=230), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=2, minutes=220), timezone.localtime()+relativedelta(days=2, minutes=230)), estado='pagada',
                                estOrigen=e, estDestino=e2, ancOrigen=e.getAnclajeByNumAnclaje(5), ancDestino=e2.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=3, minutes=40), fechaFin=timezone.localtime()+relativedelta(days=3, minutes=50), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=3, minutes=30), timezone.localtime()+relativedelta(days=3, minutes=40)), estado='pagada',
                                estOrigen=e2, estDestino=e, ancOrigen=e2.getAnclajeByNumAnclaje(1), ancDestino=e.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=3, minutes=230), fechaFin=timezone.localtime()+relativedelta(days=3, minutes=240), importe=anual.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=3, minutes=230), timezone.localtime()+relativedelta(days=3, minutes=240)), estado='pagada',
                                estOrigen=e, estDestino=e2, ancOrigen=e.getAnclajeByNumAnclaje(5), ancDestino=e2.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e2.getAnclajeByNumAnclaje(1)).first(), usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    # Debe hacer reserva de eps a renfe hoy en 5 h con usuario sgs_1970

    # Más reservas de otros usuarios entre e5 y e6
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=10, minutes=10), fechaFin=timezone.localtime()+relativedelta(days=10, minutes=20), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=10, minutes=10), timezone.localtime()+relativedelta(days=10, minutes=20)), estado='pagada',
                                estOrigen=e6, estDestino=e5, ancOrigen=e6.getAnclajeByNumAnclaje(1), ancDestino=e5.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=10, minutes=333), fechaFin=timezone.localtime()+relativedelta(days=10, minutes=343), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=10, minutes=333), timezone.localtime()+relativedelta(days=10, minutes=343)), estado='pagada',
                                estOrigen=e5, estDestino=e6, ancOrigen=e5.getAnclajeByNumAnclaje(5), ancDestino=e6.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=12, minutes=12), fechaFin=timezone.localtime()+relativedelta(days=12, minutes=23), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=12, minutes=12), timezone.localtime()+relativedelta(days=12, minutes=23)), estado='pagada',
                                estOrigen=e6, estDestino=e5, ancOrigen=e6.getAnclajeByNumAnclaje(1), ancDestino=e5.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=12, minutes=220), fechaFin=timezone.localtime()+relativedelta(days=12, minutes=230), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=12, minutes=220), timezone.localtime()+relativedelta(days=12, minutes=230)), estado='pagada',
                                estOrigen=e5, estDestino=e6, ancOrigen=e5.getAnclajeByNumAnclaje(5), ancDestino=e6.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=13, minutes=56), fechaFin=timezone.localtime()+relativedelta(days=13, minutes=66), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=13, minutes=56), timezone.localtime()+relativedelta(days=13, minutes=66)), estado='pagada',
                                estOrigen=e6, estDestino=e5, ancOrigen=e6.getAnclajeByNumAnclaje(1), ancDestino=e5.getAnclajeByNumAnclaje(5), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=13, minutes=230), fechaFin=timezone.localtime()+relativedelta(days=13, minutes=240), importe=semestral.calcularPrecioReservaTarifa(timezone.localtime()+relativedelta(days=13, minutes=230), timezone.localtime()+relativedelta(days=13, minutes=240)), estado='pagada',
                                estOrigen=e5, estDestino=e6, ancOrigen=e5.getAnclajeByNumAnclaje(5), ancDestino=e6.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e6.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Álvaro", apellidos="Martínez Sánchez").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    # Más reservas de otros usuarios entre e7 y e8
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=7, minutes=10), fechaFin=timezone.localtime()+relativedelta(days=7, minutes=20), importe=0.0, estado='pagada',
                                estOrigen=e8, estDestino=e7, ancOrigen=e8.getAnclajeByNumAnclaje(1), ancDestino=e7.getAnclajeByNumAnclaje(7), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=7, minutes=333), fechaFin=timezone.localtime()+relativedelta(days=7, minutes=343), importe=0.0, estado='pagada',
                                estOrigen=e7, estDestino=e8, ancOrigen=e7.getAnclajeByNumAnclaje(7), ancDestino=e8.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=8, minutes=12), fechaFin=timezone.localtime()+relativedelta(days=8, minutes=23), importe=0.0, estado='pagada',
                                estOrigen=e8, estDestino=e7, ancOrigen=e8.getAnclajeByNumAnclaje(1), ancDestino=e7.getAnclajeByNumAnclaje(7), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=8, minutes=220), fechaFin=timezone.localtime()+relativedelta(days=8, minutes=230), importe=0.0, estado='pagada',
                                estOrigen=e7, estDestino=e8, ancOrigen=e7.getAnclajeByNumAnclaje(7), ancDestino=e8.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()

    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=9, minutes=56), fechaFin=timezone.localtime()+relativedelta(days=9, minutes=66), importe=0.0, estado='pagada',
                                estOrigen=e8, estDestino=e7, ancOrigen=e8.getAnclajeByNumAnclaje(1), ancDestino=e7.getAnclajeByNumAnclaje(7), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()
    r1 = Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=9, minutes=230), fechaFin=timezone.localtime()+relativedelta(days=9, minutes=240), importe=0.0, estado='pagada',
                                estOrigen=e7, estDestino=e8, ancOrigen=e7.getAnclajeByNumAnclaje(7), ancDestino=e8.getAnclajeByNumAnclaje(1), bicicleta=Bicicleta.objects.filter(anclajeInicio=e8.getAnclajeByNumAnclaje(1)).first(), usuario=Usuario.objects.filter(nombre="Diego", apellidos="García García").first(), expires_at=timezone.localtime() + timedelta(minutes=10))
    r1.notificarReserva()


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
