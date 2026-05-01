from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Administrador


class AdministradorModelTest(TransactionTestCase):
    reset_sequences = True

    def test_001_administrador_str(self):
        "Prueba método str"
        usuario = UsuarioSistema(
            username="admin",
            rol="administrador")
        usuario.set_password("contraadmin")
        usuario.save()
        admin = Administrador.objects.create(
            usuario=usuario)

        self.assertEqual(str(admin), "admin (administrador)")
