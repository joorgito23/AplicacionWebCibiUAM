from django.db import models

# Create your models here.

class Pagos(models.Model):
    """
        Modelo para guardar el registro de pagos
        para que alguien no reutilice el order_id y no pague.
    """

    # Orden de pago de paypal
    order_id = models.CharField(max_length=64, unique=True)

    # Estado del pago
    pagado = models.BooleanField(default=False)