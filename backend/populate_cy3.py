import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from dateutil.relativedelta import relativedelta
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Estacion, Anclaje, Bicicleta, Contrato, Gestor
from django.utils import timezone


def populate():

    # Tarifas del sistema

    # Mensual
    mensual = Tarifa.objects.create(
        importe=30, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")

    coste = 0.5/30
    coste = round(coste, 2)

    # Semestral
    semestral = Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")

    # Anual
    anual = Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

    # Usuarios del sistema

    # Gestor
    usuario = UsuarioSistema(
        username="gestor",
        rol="gestor")
    usuario.set_password("Contracypress26$")
    usuario.save()
    Gestor.objects.create(
        usuario=usuario, nombre="luis", apellidos="perez")

    # Usuarios
    usuario2 = UsuarioSistema(
        username="usuario",
        rol="usuario")
    usuario2.set_password("Contracypress26$")
    usuario2.save()
    user = Usuario.objects.create(
        usuario=usuario2, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

    usuario3 = UsuarioSistema(
        username="usuario2",
        rol="usuario")
    usuario3.set_password("Contracypress26$")
    usuario3.save()
    user2 = Usuario.objects.create(
        usuario=usuario3, nombre="Prueba2", apellidos="Prueba2", saldo=0.0, tlf="111111111")

    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(
        days=30*6), fin=timezone.localtime().date()-relativedelta(days=1), usuario=user, tarifa=semestral)
    Contrato.objects.create(inicio=timezone.localtime().date()+relativedelta(
        days=30*6), fin=timezone.localtime().date()+relativedelta(days=30*18 - 1), usuario=user2, tarifa=anual)
    Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime().date()+relativedelta(days=30-1), usuario=user, tarifa=mensual)

    # Estación
    e = Estacion.objects.create(
        nombre="EPS", ubicacion="Campus de Cantoblanco, C. Francisco Tomás y Valiente, 11, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54719581685481,
        longitud=-3.691637357994746, nAnclajes=2)
    e.crearAnclajes()
    e1 = Estacion.objects.create(
        nombre="Facultad de Formación de Profesorado y Educación", ubicacion="C. Francisco Tomás y Valiente, 3, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54510026811934,
        longitud=-3.6966638957627427, nAnclajes=3)
    e1.crearAnclajes()

    # Bicicletas
    Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
        estacion=e1, numAnclaje=1).first(), estacionInicial=e1)
    Bicicleta.objects.create(anclajeInicio=Anclaje.objects.filter(
        estacion=e1, numAnclaje=2).first(), estacionInicial=e1)


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
