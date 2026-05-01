import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.utils import timezone
from sgu_sgs.models import Tarifa, Usuario, Contrato
from dateutil.relativedelta import relativedelta


def populate():

    # Creamos contrato de renovación
    user = Usuario.objects.filter(
       nombre="Luis", apellidos="Perez Perez").first()
    Contrato.objects.create(inicio=timezone.localtime(
    ).date()-relativedelta(days=25)+relativedelta(days=30), fin=timezone.localtime(
    ).date()-relativedelta(days=25)+relativedelta(days=30)+relativedelta(days=12*30-1), usuario=user, tarifa=Tarifa.objects.filter(duracion="anual").first())


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
