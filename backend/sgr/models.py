from django.db import models
from django.core.validators import RegexValidator
from sgu_sgs.models import Estacion, Anclaje, Usuario, Bicicleta, Notificacion
from django.utils import timezone
from datetime import timedelta
import random
import string


class Reserva(models.Model):
    """
    Modelo de una reserva de la aplicación.
    """

    # Fecha de inicio de la reserva
    fechaInicio = models.DateTimeField()

    # Fecha de fin de la reserva
    fechaFin = models.DateTimeField()

    # Código de recogida de la reserva
    codigoRecogida = models.CharField(unique=True,
                                      max_length=6,
                                      validators=[RegexValidator(
                                          r'^\d{6}$', 'El código debe tener 6 dígitos exactos')]
                                      )

    # Importe de la reserva
    importe = models.FloatField(default=0.0)

    # Estados posibles de la reserva
    est = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada')
    ]

    # Estado de la reserva
    estado = models.CharField(
        max_length=20,
        choices=est,
        default='pagada',
        blank=False,
    )

    # Estación de recogida
    estOrigen = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name='eOrigen'
    )

    # Estación de devolución
    estDestino = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name='eDestino'
    )

    # Anclaje de origen
    ancOrigen = models.ForeignKey(
        Anclaje,
        on_delete=models.CASCADE,
        related_name='aOrigen'
    )

    # Anclaje de destino
    ancDestino = models.ForeignKey(
        Anclaje,
        on_delete=models.CASCADE,
        related_name='aDestino'
    )

    # Bicicleta de la reserva
    bicicleta = models.ForeignKey(
        Bicicleta,
        on_delete=models.CASCADE,
        related_name='biciReservas'
    )

    # Usuario de la reserva
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    # Fecha de expiración de la reserva si no paga antes
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.codigoRecogida:
            self.codigoRecogida = self.generar_codigo_unico()
        super().save(*args, **kwargs)

    @staticmethod
    def generar_codigo_unico():
        """
            Genera código de reserva único
        """
        caracteres = string.ascii_uppercase + string.digits

        while True:
            codigo = ''.join(random.choice(caracteres) for _ in range(6))
            if not Reserva.objects.filter(codigoRecogida=codigo).exists():
                return codigo

    def __str__(self):
        return f"Inicio: {self.fechaInicio.strftime("%Y-%m-%d %H:%M")} - Fin: {self.fechaFin.strftime("%Y-%m-%d %H:%M")} - Codigo: {self.codigoRecogida} - Importe: {self.importe}€ - Estado: {self.estado} - Estación de origen: {self.estOrigen.nombre}, anclaje número {self.ancOrigen.numAnclaje} - Estación de destino: {self.estDestino.nombre}, anclaje número {self.ancDestino.numAnclaje} - Usuario: {self.usuario.usuario.username}"

    def notificarReserva(self):
        """
            Notifica al usuario acerca de la reserva que ha realizado.
        """

        Notificacion.objects.create(fecha=timezone.localtime().date(), usuario=self.usuario,
                                    msg=f"A continuación se indica un resumen de su reserva. Inicio: {timezone.localtime(self.fechaInicio).strftime("%Y-%m-%d %H:%M")} - Fin: {timezone.localtime(self.fechaFin).strftime("%Y-%m-%d %H:%M")}. Origen: {self.estOrigen.nombre} nº {self.ancOrigen.numAnclaje} - Destino: {self.estDestino.nombre} nº {self.ancDestino.numAnclaje}. Código de recogida: {self.codigoRecogida}")

    def esCancelable(self):
        """
            Determina si una reserva es cancelable o no.

            RETURN:
                boolean: True si es cancelable o False en caso contrario
        """

        # Obtenemos fecha y hora actual.
        unaHoraMas = timezone.localtime() + timedelta(hours=1)

        # Si cancela con una hora de antelación y está pagada es cancelable
        if unaHoraMas > self.fechaInicio or self.estado != 'pagada':
            return False

        return True

    def actualizarEstado(self, estado):
        """
            Actualiza el estado de la reserva.

            ARGS:
                estado: estado a actualizar
        """

        # Actualiza estado de la reserva
        self.estado = estado
        self.save()

    def devolverImporte(self):
        """
            Reembolsa al usuario el importe de la reserva.
        """

        # Reembolso de importe
        self.usuario.actualizarSaldo(self.importe)

    def cancelar(self):
        """
            Cancela una reserva realizada anteriormente.
        """

        # Actualiza estado de la reserva
        self.actualizarEstado("cancelada")

        # Reembolsa el importe al usuario
        self.devolverImporte()
