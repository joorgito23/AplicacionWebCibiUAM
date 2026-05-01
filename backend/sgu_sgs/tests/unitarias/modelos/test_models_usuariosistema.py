from django.test import TransactionTestCase
from sgu_sgs.models import UsuarioSistema, Usuario, Gestor, Administrador


class UsuarioSistemaModelTest(TransactionTestCase):
    reset_sequences = True

    def test_001_usuarioSistema_str(self):
        """
        Prueba método str
        """
        usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        usuario.set_password("contrausuario")
        usuario.save()
        self.assertEqual(str(usuario), "usuario (usuario)")

    def test_002_usuarioSistema_getRol(self):
        """
        Prueba método getRol
        """

        # Comprueba que devuelve el rol correcto
        usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        usuario.set_password("contrausuario")
        usuario.save()
        self.assertEqual(usuario.getRol(), "usuario")

    def test_003_usuarioSistema_obtenerPerfilCompleto(self):
        """
        Prueba método obtenerPerfilCompleto
        """

        # Comprueba que devuelve la instancia completa del usuario
        usuario = UsuarioSistema(
            username="usuario",
            rol="usuario")
        usuario.set_password("contrausuario")
        usuario.save()
        user = Usuario.objects.create(
            usuario=usuario, nombre="Prueba", apellidos="Prueba", saldo=0.0, tlf="111111111")

        self.assertEqual(usuario.obtenerPerfilCompleto(), user)

    def test_004_usuarioSistema_obtenerPerfilCompleto(self):
        """
        Prueba método obtenerPerfilCompleto
        """

        # Comprueba que devuelve la instancia completa del gestor
        usuario = UsuarioSistema(
            username="gestor",
            rol="gestor")
        usuario.set_password("contragestor")
        usuario.save()
        gestor = Gestor.objects.create(
            usuario=usuario, nombre="Prueba2", apellidos="Prueba2")

        self.assertEqual(usuario.obtenerPerfilCompleto(), gestor)

    def test_005_usuarioSistema_obtenerPerfilCompleto(self):
        """
        Prueba método obtenerPerfilCompleto
        """

        # Comprueba que devuelve la instancia completa del administrador
        usuario = UsuarioSistema(
            username="admin",
            rol="administrador")
        usuario.set_password("contraadmin")
        usuario.save()
        admin = Administrador.objects.create(
            usuario=usuario)

        self.assertEqual(usuario.obtenerPerfilCompleto(), admin)
