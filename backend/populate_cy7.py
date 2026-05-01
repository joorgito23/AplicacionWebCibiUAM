import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.utils import timezone
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Estacion, Anclaje, Bicicleta, Contrato, Gestor
from sgr.models import Reserva
from dateutil.relativedelta import relativedelta
from datetime import timedelta


def populate():

    # Tarifas
    Tarifa.objects.create(
        importe=30, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")
    coste = round(0.5/30, 2)
    semestral = Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")
    Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

    # Usuario
    usuario = UsuarioSistema(
        username="usuario",
        rol="usuario")
    usuario.set_password("Contracypress26$")
    usuario.save()
    user = Usuario.objects.create(
        usuario=usuario, nombre="Prueba", apellidos="Prueba", saldo=5.0, tlf="111111111")
    Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime(
    ).date()+relativedelta(days=29), usuario=user, tarifa=semestral)

    # Estaciones y bicicletas
    est = Estacion.objects.create(
        nombre="Estación 1", ubicacion="Prueba", latitud=0,
        longitud=0.5, nAnclajes=2)
    anc = Anclaje.objects.create(estacion=est, numAnclaje=1)
    Anclaje.objects.create(estacion=est, numAnclaje=2)
    bici = Bicicleta.objects.create(
        estacionInicial=est, anclajeInicio=anc)
    est2 = Estacion.objects.create(
        nombre="Estación 2", ubicacion="Prueba2", latitud=3,
        longitud=0.5, nAnclajes=2)
    anc3 = Anclaje.objects.create(estacion=est2, numAnclaje=1)
    Anclaje.objects.create(estacion=est2, numAnclaje=2)

    # Gestor
    usuario2 = UsuarioSistema(
        username="gestor",
        rol="gestor")
    usuario2.set_password("Contracypress26$")
    usuario2.save()
    Gestor.objects.create(
        usuario=usuario2)

    # Usuario
    usuario3 = UsuarioSistema(
        username="usuario2",
        rol="usuario")
    usuario3.set_password("Contracypress26$")
    usuario3.save()
    user2 = Usuario.objects.create(
        usuario=usuario3, nombre="Prueba", apellidos="Prueba", saldo=5.0, tlf="111111111")

    # Reserva
    Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=1), fechaFin=timezone.localtime()+relativedelta(days=1, minutes=10), importe=5, estado='pagada',
                           estOrigen=est, estDestino=est2, ancOrigen=anc, ancDestino=anc3, bicicleta=bici, usuario=user, expires_at=timezone.localtime() + timedelta(minutes=10))

    Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=3), fechaFin=timezone.localtime()+relativedelta(days=3, minutes=10), importe=4, estado='pagada',
                           estOrigen=est, estDestino=est2, ancOrigen=anc, ancDestino=anc3, bicicleta=bici, usuario=user, expires_at=timezone.localtime() + timedelta(minutes=10))

    Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(days=2), fechaFin=timezone.localtime()+relativedelta(days=2, minutes=10), importe=3, estado='pagada',
                           estOrigen=est2, estDestino=est, ancOrigen=anc3, ancDestino=anc, bicicleta=bici, usuario=user2, expires_at=timezone.localtime() + timedelta(minutes=10))


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
