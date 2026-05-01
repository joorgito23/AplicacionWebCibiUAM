import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from dateutil.relativedelta import relativedelta
from sgu_sgs.models import UsuarioSistema, Tarifa, Usuario, Contrato
from django.utils import timezone


def populate():

    # Simulamos que creamos usuario
    usuarioSistema2 = UsuarioSistema(username="cypress", rol="usuario")
    usuarioSistema2.set_password("Contracypress26$")
    usuarioSistema2.save()
    usuario = Usuario.objects.create(
        usuario=usuarioSistema2, nombre="Luis", apellidos="Gonzalez Gonzalez", tlf="111222333", saldo=0.0)
    Contrato.objects.create(inicio=timezone.localtime().date(), fin=timezone.localtime().date()+relativedelta(days=29), usuario=usuario, tarifa=Tarifa.objects.filter(duracion="mensual").first())


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
