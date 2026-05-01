import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from sgu_sgs.models import Tarifa, Estacion, Anclaje, Bicicleta


def populate():

    # Tarifas del sistema

    # Mensual
    Tarifa.objects.create(
        importe=30, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")

    coste = 0.5/30
    coste = round(coste, 2)

    # Semestral
    Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")

    # Anual
    Tarifa.objects.create(importe=10, precioMinuto=coste,
                          descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

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
