import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from dateutil.relativedelta import relativedelta
from sgu_sgs.models import Usuario, Estacion, Bicicleta
from sgr.models import Reserva
from django.utils import timezone


def populate():
    e = Estacion.objects.filter(nombre="Facultad de Formación de Profesorado y Educación").first()
    e1 = Estacion.objects.filter(nombre="EPS").first()
    a = e.getAnclajeByNumAnclaje(1)
    a1 = e1.getAnclajeByNumAnclaje(1)
    b = Bicicleta.objects.all().first()

    # Simulamos que creamos reserva
    Reserva.objects.create(fechaInicio=timezone.localtime()+relativedelta(minutes=90), fechaFin=timezone.localtime()+relativedelta(minutes=100), importe=0.2, estado='pagada',
                           estOrigen=e, estDestino=e1, ancOrigen=a, ancDestino=a1, bicicleta=b, usuario=Usuario.objects.all().first(), expires_at=timezone.localtime())


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
