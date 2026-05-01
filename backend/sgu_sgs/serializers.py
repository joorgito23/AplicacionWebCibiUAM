
from .models import UsuarioSistema
from rest_framework import serializers
from .models import Gestor, Anclaje, Bicicleta, Estacion, Contrato, Notificacion, Tarifa, UsuarioPendiente, Usuario, usuarioExistente, getTarifaByName
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import TokenSerializer


class CustomTokenSerializer(TokenSerializer):
    """
    Serializer para que Djoser devuelva el rol del usuario
    junto con el token de acceso.
    """
    rol = serializers.CharField(source="user.rol", read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ("rol",)


class TarifaSerializer(serializers.ModelSerializer):
    """
    Serializer para devolver la información de una tarifa
    con los campos deseados.
    """
    class Meta:
        model = Tarifa
        fields = ('importe', 'precioMinuto', 'descripcion', 'duracion')


class TarifaListaSerializer(serializers.ModelSerializer):
    """
    Serializer para devolver la duración de las tarifas
    disponibles y mostrar una lista de las opciones.
    """
    class Meta:
        model = Tarifa
        fields = ['duracion']


class EstacionSerializer(serializers.ModelSerializer):
    """
    Serializer para obtener la información de una estación del campus.
    """
    class Meta:
        model = Estacion
        fields = ['nombre', 'ubicacion', 'nAnclajes', 'latitud', 'longitud']


class BicicletaSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar los id de todas las bicicletas en un listado.
    """
    class Meta:
        model = Bicicleta
        fields = ['id']


class NotificacionSerializer(serializers.ModelSerializer):
    """
    Serializer para devolver el contenido de las notificaciones de un
    usuario con su fecha de envío.
    """
    class Meta:
        model = Notificacion
        fields = ('fecha', 'msg')


class UsuarioSistemaNombreSerializer(serializers.ModelSerializer):
    """
    Serializer de un usuario del sistema.
    """
    class Meta:
        model = UsuarioSistema
        fields = ['username']


class TarifaNombreSerializer(serializers.ModelSerializer):
    """
    Serializer de una tarifa para la información de un contrato.
    """
    class Meta:
        model = Tarifa
        fields = ['duracion']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer de un usuario.
    """
    usuario = UsuarioSistemaNombreSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['usuario']


class ContratoSerializer(serializers.ModelSerializer):
    """
    Serializer de un contrato.
    """
    usuario = UsuarioSerializer(read_only=True)
    tarifa = TarifaNombreSerializer(read_only=True)

    class Meta:
        model = Contrato
        fields = ('id', 'usuario', 'inicio', 'fin', 'tarifa')


class UsuarioPendienteSerializer(serializers.ModelSerializer):
    """
    Serializer de un usuario temporal del sistema antes del pago.
    """
    contraseña = serializers.CharField(write_only=True)
    tarifa = serializers.CharField()

    class Meta:
        model = UsuarioPendiente
        fields = "__all__"
        read_only_fields = ['expires_at']

    def validate_usuario(self, usuario):
        """
        Método de validación de un usuario. Verifica que no exista en el sistema.

        ARGS:
            usuario: nombre de usuario

        RETURN:
            usuario: nombre de usuario

        """

        # Verifica la existencia del usuario
        if usuarioExistente(usuario):
            raise serializers.ValidationError("El nombre de usuario ya existe")
        if UsuarioPendiente.objects.filter(usuario=usuario).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return usuario

    def validate_contraseña(self, contraseña):
        """
        Método de validación de una contraseña.

        ARGS:
            contraseña: contraseña del nuevo usuario

        RETURN:
            contraseña: contraseña del nuevo usuario

        """

        try:
            validate_password(contraseña)
        except Exception:
            raise serializers.ValidationError(
                "La contraseña no cumple los requisitos de seguridad")
        return contraseña

    def validate_tarifa(self, tarifa):
        """
        Método de validación de una tarifa.

        ARGS:
            tarifa: tarifa del nuevo usuario

        RETURN:
            t: instancia de la tarifa

        """

        # Obtención tarifa a partir del nombre
        t = getTarifaByName(tarifa)
        if t is None:
            raise serializers.ValidationError("Tarifa no existente")

        return t
    

class GestorSerializer(serializers.ModelSerializer):
    """
    Serializer de un gestor para mostrar una lista de los existentes
    """
    usuario = UsuarioSistemaNombreSerializer(read_only=True)

    class Meta:
        model = Gestor
        fields = ['usuario', 'nombre', 'apellidos']


class EstacionReservaSerializer(serializers.ModelSerializer):
    """
    Serializer para obtener la información de una estación del campus para una reserva.
    """
    class Meta:
        model = Estacion
        fields = ['nombre']


class AnclajeSerializer(serializers.ModelSerializer):
    """
    Serializer para obtener la información de una anclaje del campus para una reserva.
    """
    class Meta:
        model = Anclaje
        fields = ['numAnclaje']
