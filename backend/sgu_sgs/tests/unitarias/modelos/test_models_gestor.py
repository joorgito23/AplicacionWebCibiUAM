from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Gestor


class GestorModelTest(TransactionTestCase):
    reset_sequences = True

    def test_001_gestor_str(self):
        """
        Prueba método str
        """
        usuario = UsuarioSistema(
            username="gestor",
            rol="gestor")
        usuario.set_password("contragestor")
        usuario.save()
        gestor = Gestor.objects.create(
            usuario=usuario, nombre="Prueba2", apellidos="Prueba2")

        self.assertEqual(str(gestor), "gestor (gestor) - Prueba2 Prueba2")
