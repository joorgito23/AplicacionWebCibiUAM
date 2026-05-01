from rest_framework import serializers
from .models import Reserva
from sgu_sgs.serializers import UsuarioSerializer, AnclajeSerializer, EstacionReservaSerializer


class ReservaSerializer(serializers.ModelSerializer):
    """
    Serializer de una reserva.
    """
    usuario = UsuarioSerializer(read_only=True)
    estOrigen = EstacionReservaSerializer(read_only=True)
    estDestino = EstacionReservaSerializer(read_only=True)
    ancOrigen = AnclajeSerializer(read_only=True)
    ancDestino = AnclajeSerializer(read_only=True)
    fechaInicio = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M"
    )
    fechaFin = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M"
    )

    class Meta:
        model = Reserva
        fields = ('id', 'usuario', 'fechaInicio', 'fechaFin', 'codigoRecogida',
                  'importe', 'estado', 'estOrigen', 'estDestino', 'ancOrigen', 'ancDestino')
