import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from dateutil.relativedelta import relativedelta
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Estacion, Anclaje, Bicicleta, Contrato
from django.utils import timezone


def populate():

    # Tarifas
    Tarifa.objects.create(importe=30, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")
    coste = round(0.5/30, 2)
    semestral = Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")
    Tarifa.objects.create(importe=10, precioMinuto=coste, descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

    # Estaciones
    e = Estacion.objects.create(
        nombre="EPS", ubicacion="Campus de Cantoblanco, C. Francisco Tomás y Valiente, 11, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54719581685481,
        longitud=-3.691637357994746, nAnclajes=2)
    e.crearAnclajes()
    e1 = Estacion.objects.create(
        nombre="Facultad de Formación de Profesorado y Educación", ubicacion="C. Francisco Tomás y Valiente, 3, Fuencarral-El Pardo, 28049 Madrid", latitud=40.54510026811934,
        longitud=-3.6966638957627427, nAnclajes=3)
    anc = Anclaje.objects.create(estacion=e1, numAnclaje=1)
    Anclaje.objects.create(estacion=e1, numAnclaje=2)
    Anclaje.objects.create(estacion=e1, numAnclaje=3)

    # Bicicleta
    Bicicleta.objects.create(
        estacionInicial=e1, anclajeInicio=anc)

    # Usuario
    usuario = UsuarioSistema(
        username="usuario",
        rol="usuario")
    usuario.set_password("Contracypress26$")
    usuario.save()
    user = Usuario.objects.create(
        usuario=usuario, nombre="Luis", apellidos="Perez Perez", saldo=0.0, tlf="111111111")
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
    ).date()-relativedelta(days=25)+relativedelta(days=179), usuario=user, tarifa=semestral)


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
