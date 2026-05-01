import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.utils import timezone
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Estacion, Anclaje, Bicicleta, Notificacion, Contrato
from dateutil.relativedelta import relativedelta


def populate():

    # Tarifas del sistema

    # Mensual
    mensual = Tarifa.objects.create(
        importe=30, precioMinuto=0, descripcion="Esta tarifa permite realizar un número de reservas ilimitadas a coste 0.", duracion="mensual")

    coste = 0.5/30
    coste = round(coste, 2)

    # Semestral
    Tarifa.objects.create(
        importe=10, precioMinuto=coste, descripcion="Esta tarifa permite realizar reservas con un coste bajo.", duracion="semestral")

    # Anual
    Tarifa.objects.create(importe=10, precioMinuto=coste,
                          descripcion="Esta tarifa permite hacer un renovacion al año y olvidarte", duracion="anual")

    # Usuarios del sistema

    # Usuario
    usuario = UsuarioSistema(
        username="usuario",
        rol="usuario")
    usuario.set_password("Contracypress26$")
    usuario.save()
    user = Usuario.objects.create(
        usuario=usuario, nombre="Luis", apellidos="Perez Perez", saldo=0.0, tlf="111111111")
    Contrato.objects.create(inicio=timezone.localtime().date()-relativedelta(days=25), fin=timezone.localtime(
    ).date()-relativedelta(days=25)+relativedelta(days=29), usuario=user, tarifa=mensual)

    # Notificaciones del usuario
    Notificacion.objects.create(fecha=timezone.localtime().date(
    )-relativedelta(days=30*12), msg="Prueba 1", usuario=user)
    Notificacion.objects.create(fecha=timezone.localtime().date(
    )-relativedelta(days=30), msg="Prueba 2", usuario=user)

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
