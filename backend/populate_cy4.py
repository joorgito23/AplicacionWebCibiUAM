import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from sgu_sgs.models import Administrador, UsuarioSistema, Gestor


def populate():

    # Usuarios del sistema

    # Administrador
    usuario = UsuarioSistema(
        username="admin",
        rol="administrador")
    usuario.set_password("Contracypress26$")
    usuario.save()
    Administrador.objects.create(
        usuario=usuario)

    # Gestor
    usuario2 = UsuarioSistema(
        username="gestorPrueba",
        rol="gestor")
    usuario2.set_password("Contracypress26$")
    usuario2.save()
    Gestor.objects.create(
        usuario=usuario2, nombre="luis", apellidos="perez")


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Done!")
