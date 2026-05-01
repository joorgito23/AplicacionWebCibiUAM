from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
from django.forms import ValidationError
from math import floor


class UsuarioSistema(AbstractUser):

    """
        Modelo genérico para los diferentes usuarios del sistema con los
        datos comunes a los 3 roles existentes.
    """

    CHOICES = [
        ('usuario', 'Usuario'),
        ('gestor', 'Gestor'),
        ('administrador', 'Administrador'),
    ]

    # Rol del usuario
    rol = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='usuario',
        blank=False,
    )

    def __str__(self):

        return f"{self.username} ({self.rol})"

    def getRol(self):
        """
            Obtener rol del usuario

            RETURN:
                str: rol del usuario: usuario, gestor o administrador
        """
        return self.rol

    def obtenerPerfilCompleto(self):
        """
            Devuelve la instancia completa del usuario

            RETURN:
                Usuario: si rol es usuario
                Gestor: si rol es gestor
                Administrador: si rol es administrador
        """
        if self.rol == "usuario":
            return self.usuario
        elif self.rol == "gestor":
            return self.gestor
        return self.administrador


class Gestor(models.Model):
    """
        Modelo de un gestor.
    """
    # Instancia del modelo UsuarioSistema que contiene el rol, usuario y contraseña
    usuario = models.OneToOneField(UsuarioSistema, on_delete=models.CASCADE)

    # Nombre del gestor
    nombre = models.CharField(max_length=100)

    # Apellidos del gestor
    apellidos = models.CharField(max_length=150)

    def __str__(self):
        return str(self.usuario) + f" - {self.nombre} {self.apellidos}"


class Administrador(models.Model):
    """
        Modelo de un administrador.
    """
    # Instancia del modelo UsuarioSistema que contiene el rol, usuario y contraseña
    usuario = models.OneToOneField(UsuarioSistema, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario)


class Usuario(models.Model):
    """
        Modelo de un usuario.
    """
    # Instancia del modelo UsuarioSistema que contiene el rol, usuario y contraseña
    usuario = models.OneToOneField(UsuarioSistema, on_delete=models.CASCADE)

    # Nombre del usuario
    nombre = models.CharField(max_length=100)

    # Apellidos del usuario
    apellidos = models.CharField(max_length=150)

    # Saldo restante del usuario
    saldo = models.FloatField(default=0.0)

    # Teléfono del usuario
    tlf = models.CharField(
        max_length=9,
        validators=[RegexValidator(
            r'^\d{9}$', 'El teléfono debe tener 9 dígitos exactos')]
    )

    def __str__(self):
        return str(self.usuario) + f" - {self.nombre} {self.apellidos}, {self.tlf}. Saldo: {self.saldo}"

    def getPerfil(self):
        """
            Obtener los datos asociados al perfil del usuario.

            RETURN:
                json: contiene usuario, nombre, apellidos, rol, fecha fin del contrato, tarifa actual, saldo y teléfono
        """
        # Obtiene contrato actual del usuario
        contrato = self.getContratoActual()
        if contrato is None:
            return {"usuario": self.usuario.username, "nombre": self.nombre, "apellidos": self.apellidos, "rol": self.usuario.getRol(), "duracion": "Sin tarifa contratada actualmente", "fin": "Sin tarifa contratada actualmente", "saldo": self.saldo, "tlf": self.tlf}

        return {"usuario": self.usuario.username, "nombre": self.nombre, "apellidos": self.apellidos, "rol": self.usuario.getRol(), "duracion": contrato.tarifa.getDuracion().capitalize(), "fin": contrato.getFin(), "saldo": self.saldo, "tlf": self.tlf}

    def modificarPerfil(self, tlf):
        """
            Modifica el número de teléfono del usuario.

            ARGS:
                tlf: nuevo número de teléfono

            RETURN:
                bool: booleano que indica si se puede actualizar o no
        """

        # Comprueba si el nuevo número de teléfono es correcto
        if self.verificarTlf(tlf) is False:
            return False

        self.tlf = tlf
        self.save()
        return True

    def verificarTlf(self, tlf):
        """
            Valida si un número de teléfono es correcto.

            ARGS:
                tlf: nuevo número de teléfono

            RETURN:
                bool: booleano que indica si es válido o no
        """
        validator = RegexValidator(
            r'^\d{9}$', 'El teléfono debe tener 9 dígitos exactos')

        try:
            validator(tlf)
        except ValidationError:
            return False

        return True

    def getContratoActual(self):
        """
            Obtiene el contrato actual del usuario.

            RETURN:
                Contrato: contrato actual
                None: si no tiene contrato actualmente
        """
        hoy = timezone.localtime().date()
        return self.contratos.filter(inicio__lte=hoy, fin__gte=hoy).first()

    def calcularFechaFinContrato(self, fecha, tarifa):
        """
            Calcula la fecha fin de un contrato a partir de la fecha de inicio y la tarifa.

            ARGS:
                fecha: fecha de inicio del contrato
                tarifa: tarifa del contrato

            RETURN:
                date: fecha fin del contrato
        """

        # Calcula duración
        fin = tarifa.calcularFechaFin(fecha)

        return fin

    def crearContrato(self, tarifa):
        """
            Crea un nuevo contrato al usuario.

            ARGS:
                tarifa: tarifa del contrato

        """
        # Calcula fecha fin del contrato
        hoy = timezone.localtime().date()
        fin = self.calcularFechaFinContrato(hoy, tarifa)
        # Crea nuevo contrato
        Contrato.objects.create(inicio=hoy, fin=fin,
                                usuario=self, tarifa=tarifa)

    def getFechaInicioContrato(self):
        """
            Obtiene la fecha de inicio del siguiente contrato.

            RETURN:
                date: fecha de inicio del nuevo contrato a crear
        """

        # Ordena contratos del usuario por fecha descendente
        c = self.contratos.all().order_by("-fin").first()

        # Calcula fecha de inicio en función de la fecha fin del último contrato
        if c is None:
            return timezone.localtime().date()
        fin = c.getFin()
        if fin < timezone.localtime().date():
            inicio = timezone.localtime().date()
        else:
            inicio = fin + timedelta(days=1)
        return inicio

    def renovarContrato(self, tarifa):
        """
            Renueva el contrato del usuario.

            ARGS:
                tarifa: tarifa del nuevo contrato

        """
        # Calcular fecha inicio del contrato
        inicio = self.getFechaInicioContrato()

        # Calcular fecha fin del contrato
        fin = self.calcularFechaFinContrato(inicio, tarifa)

        # Creación del nuevo contrato
        Contrato.objects.create(inicio=inicio, fin=fin,
                                usuario=self, tarifa=tarifa)

    def avisarExpiracionContrato(self):
        """
            Genera la notificación de aviso de fin de contrato en caso de ser necesario
            y no haber sido creada previamente.


            RETURN:
                bool: booleano que indica si se creó la notificación o no
        """

        # Obtiene contrato actual
        c = self.getContratoActual()

        # Si hay contrato, y caduca en menos de 10 días y no se ha creado antes, crea la notificación
        if c is not None:
            if c.getFin() <= timezone.localtime().date() + relativedelta(days=10):
                n = Notificacion.objects.filter(fecha=c.getFin() - relativedelta(days=10), usuario=self,
                                                msg__icontains="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.").first()
                if n is None:
                    Notificacion.objects.create(fecha=c.getFin() - relativedelta(days=10), usuario=self,
                                                msg="Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación.")
                    return True
        return False

    def reservaPosible(self, fechaInicio, fechaFin):
        """
            Determina si un usuario puede realizar una reserva con las condiciones indicadas.
            En caso de que exista otra reserva en esa franja temporal, no permitirá la reserva.

            ARGS:
                fechaInicio: fecha de inicio de la reserva deseada
                fechaFin: fecha de fin de la reserva deseada

            RETURN:
                bool: booleano que indica si el usuario puede realizar la reserva o no
        """

        # Validamos fecha
        if fechaInicio > fechaFin:
            return False

        # Verficamos que el usuario tenga contrato
        contrato = self.getContratoActual()
        if contrato is None:
            return False

        # Buscamos solape de reservas con las condiciones deseadas del usuario

        # Obtener reservas del usuario cuyo fin está en la franja temporal de la reserva deseada
        reservas = self.reservas.filter(
            fechaFin__gte=fechaInicio, fechaFin__lte=fechaFin, estado='pagada')

        # Si hay coincidencia no es posible la reserva
        if reservas:
            return False

        # Obtener reservas del usuario cuyo inicio está en la franja temporal de la reserva deseada
        reservas = self.reservas.filter(
            fechaInicio__gte=fechaInicio, fechaInicio__lte=fechaFin, estado='pagada')

        # Si hay coincidencia no es posible la reserva
        if reservas:
            return False

        return True

    def calcularPrecioReservaUsuario(self, fechaInicio, fechaFin):
        """
            Determina el importe de una reserva en función de su duración.

            ARGS:
                fechaInicio: fecha de inicio de la reserva deseada
                fechaFin: fecha de fin de la reserva deseada

            RETURN:
                float: importe de la reserva
        """

        # Verificamos validez de fechas
        if fechaInicio > fechaFin:
            return -1

        # Obtenemos contrato actual
        c = self.getContratoActual()

        # Error si no tiene contrato
        if c is None:
            return -1

        # Obtenemos tarifa del contrato y calculamos importe
        tarifa = c.tarifa
        return tarifa.calcularPrecioReservaTarifa(fechaInicio, fechaFin)

    def precioReservaSaldo(self, importe):
        """
            Determina el importe final de una reserva descontando saldo del usuario.

            ARGS:
                importe: precio inicial de la reserva

            RETURN:
                float: importe de la reserva
        """

        # Validamos importe
        if importe < 0:
            return -1

        # Devolvemos precio final
        if importe >= self.saldo:
            return round(importe - self.saldo, 2)

        return round(0, 2)

    def actualizarSaldo(self, cantidad):
        """
            Actualiza el saldo del usuario.

            ARGS:
                cantidad: importe a sumar o descontar

            RETURN:
                boolean: True si se actualizó correctamente o False en caso contrario
        """

        # Actualizamos saldo
        if abs(cantidad) > self.saldo and cantidad < 0:
            self.saldo = round(0, 2)
        else:
            self.saldo = round(self.saldo + cantidad, 2)

        self.save()
        return True

    def getReservaById(self, idReserva):
        """
            Obtiene una reserva del usuario a partir del id de la reserva

            ARGS:
                idReserva: id de la reserva

            RETURN:
                Reserva: reserva deseada
                None: si no existe una reserva realizada por el usuario con ese id
        """

        # Buscamos reserva del usuario con ese id
        reserva = self.reservas.filter(id=idReserva).first()

        return reserva

    def getReservas(self):
        """
            Obtiene las reservas del usuario

            RETURN:
                List<Reserva>: reservas del usuario
        """

        # Devolvemos reservas
        return self.reservas.filter(estado__in=['pagada', 'cancelada']).order_by('-fechaInicio')


class Estacion(models.Model):
    """
        Modelo de una estación del campus.
    """

    # Nombre de la estación
    nombre = models.CharField(unique=True, max_length=128)

    # Ubicación de la estación
    ubicacion = models.CharField(max_length=512)

    # Número de anclajes de la estación
    nAnclajes = models.IntegerField(default=5)

    # Latitud
    latitud = models.DecimalField(max_digits=20, decimal_places=17)

    # Longitud
    longitud = models.DecimalField(max_digits=20, decimal_places=17)

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}: {self.nAnclajes} anclajes"

    def crearAnclajes(self):
        """
            Crea los anclajes asociados a la nueva estación.
        """

        # Creación de los anclajes asociados a la estación
        for i in range(1, self.nAnclajes + 1):
            Anclaje.objects.create(numAnclaje=i, estacion=self)

    def getAnclajeByNumAnclaje(self, numAnclaje):
        """
            Obtiene el anclaje de la estación cuyo número es numAnclaje.

            ARGS:
                numAnclaje: número del anclaje en la estación

            RETURN:
                Anclaje: anclaje cuyo número es numAnclaje
                None: en caso de que no exista
        """

        # Busca y devuelve el anclaje solicitado
        return self.anclajes.filter(numAnclaje=numAnclaje).first()

    def getDisponibilidadAnclajeBicicleta(self):
        """
            Calcula el número de bicicletas y anclajes disponibles de la estación en el
            momento actual.

            RETURN:
                json: contiene número de anclajes libres y número de bicicletas libres.
        """

        anclajeLibre = 0
        anclajeOcupado = 0

        # Cálculo de la disponibilidad de la estación
        # Para cada anclaje se obtiene si está libre o no
        for a in self.anclajes.all():
            # Obtención disponibilidad anclaje
            resp = a.anclajeLibre()

            if resp:
                anclajeLibre = anclajeLibre+1
            else:
                anclajeOcupado = anclajeOcupado+1
        return {"libre": anclajeLibre, "ocupado": anclajeOcupado}

    def seleccionarAnclajeOrigen(self, fechaInicio):
        """
            Obtiene el anclaje origen para la reserva a partir de los datos de entrada

            ARGS:
                fechaInicio: fecha de inicio de la reserva


            RETURN:
                Anclaje: anclaje de origen reservado
                None: en caso de que no haya ningún anclaje disponible para la reserva
        """

        # Obtenemos anclajes de la estación
        anclajes = self.anclajes.all()

        # Recorremos los anclajes y buscamos si alguno puede ser el anclaje de origen
        for a in anclajes:

            # Si hay una bicicleta disponible en el anclaje
            if a.anclajeDisponibleRecogida(fechaInicio):
                return a

        return None

    def seleccionarAnclajeDestino(self, fechaFin):
        """
            Obtiene el anclaje destino para la reserva a partir de los datos de entrada

            ARGS:
                fechaFin: fecha de fin de la reserva


            RETURN:
                Anclaje: anclaje de destino reservado
                None: en caso de que no haya ningún anclaje disponible para la reserva
        """

        # Obtenemos anclajes de la estación
        anclajes = self.anclajes.all()

        # Recorremos los anclajes y buscamos si alguno puede ser el anclaje de destino
        for a in anclajes:

            # Si no hay una bicicleta en el anclaje
            if a.anclajeDisponibleAsignacion(fechaFin):
                return a

        return None


class Anclaje(models.Model):
    """
        Modelo de un anclaje del campus.
    """

    # Número de anclaje en la estación
    numAnclaje = models.IntegerField()

    # Estación asociada
    estacion = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name='anclajes'
    )

    def __str__(self):
        return f"Anclaje número {self.numAnclaje} de la estación {self.estacion.nombre}"

    def anclajeLibre(self):
        """
            Obtiene si un anclaje no tiene anclada ninguna bicicleta en el momento actual.

            RETURN:
                bool: True si está libre y False en caso contrario
        """

        # Primero miramos si se ha asignado una bicicleta inicial en ese anclaje
        bicis = Bicicleta.objects.filter(anclajeInicio=self).order_by('-fecha')

        if not bicis:
            # Obtenemos las reservas anteriores a la hora actual en las que el anclaje es origen o destino
            reservasDest = self.aDestino.filter(
                fechaFin__lte=timezone.localtime(), estado__in=['pagada', 'cancelada'])
            reservasOrig = self.aOrigen.filter(
                fechaInicio__lt=timezone.localtime(), estado__in=['pagada', 'cancelada'])

            reservas = reservasDest | reservasOrig
            reservas = reservas.order_by('-fechaFin')

            # Si no hay reservas está libre
            if not reservas:

                return True

            # Si hay reservas anteriores, si la última es destino ocupado
            últimaReserva = reservas.first()
            if últimaReserva.ancDestino == self:
                return False

            # Si la última es origen, está libre
            return True

        # Si hay bicicletas que tienen este anclaje como inicial
        # Obtenemos la bicicleta asignada más recientemente
        bici = bicis.first()
        fechaCreacion = bici.fecha

        # Buscamos reservas anteriores al momento actual y posterior a la creación de la bicicleta
        reservasDest = self.aDestino.filter(
            fechaFin__gt=fechaCreacion, fechaFin__lte=timezone.localtime(), estado__in=['pagada', 'cancelada'])
        reservasOrig = self.aOrigen.filter(
            fechaInicio__gt=fechaCreacion, fechaInicio__lte=timezone.localtime(), estado__in=['pagada', 'cancelada'])

        reservas = reservasDest | reservasOrig
        reservas = reservas.order_by('-fechaFin')

        # Si no hay reservas anteriores no está libre
        if not reservas:
            return False

        # Si hay reservas anteriores, si la última es destino ocupado
        últimaReserva = reservas.first()
        if últimaReserva.ancDestino == self:
            return False

        # Si la utlima previa es origen está libre

        return True

    def anclajeDisponibleAsignacion(self, fecha):
        """
            Obtiene si un anclaje está libre y puede anclarse una bicicleta o no en la fecha y hora indicadas.

            ARGS:
                fecha: fecha que se desea conocer disponibilidad

            RETURN:
                bool: True si está libre y False en caso contrario
        """

        # Si el anclaje está implicado en alguna reserva pendiente de pago no lo usamos
        rDest = self.aDestino.filter(estado='pendiente')
        rOrig = self.aOrigen.filter(estado='pendiente')
        if rDest or rOrig:
            return False

        # Primero miramos si se ha asignado una bicicleta inicial en ese anclaje
        bicis = Bicicleta.objects.filter(anclajeInicio=self).order_by('-fecha')

        if not bicis:
            # Obtenemos las reservas anteriores a la hora actual en las que el anclaje es origen o destino
            reservasDest = self.aDestino.filter(
                fechaFin__lte=fecha, estado__in=['pagada', 'cancelada'])
            reservasOrig = self.aOrigen.filter(
                fechaInicio__lt=fecha, estado__in=['pagada', 'cancelada'])

            reservas = reservasDest | reservasOrig
            reservas = reservas.order_by('-fechaFin')

            # Si no hay reservas y no hay reservas después que sea destino está libre
            if not reservas:
                reservasDestPost = self.aDestino.filter(
                    fechaFin__gte=fecha, estado__in=['pagada', 'cancelada'])
                if not reservasDestPost:
                    return True

                return False

            # Si hay reservas anteriores, si la última es destino ocupado
            últimaReserva = reservas.first()
            if últimaReserva.ancDestino == self:
                return False

            # Si la última es origen, está libre si no hay reservas después en la que sea destino
            reservasDestPost = self.aDestino.filter(
                fechaFin__gte=fecha, estado__in=['pagada', 'cancelada'])
            if not reservasDestPost:
                return True

            return False

        # Si hay bicicletas que tienen este anclaje como inicial
        # Obtenemos la bicicleta asignada más recientemente
        bici = bicis.first()
        fechaCreacion = bici.fecha

        # Buscamos reservas anteriores al momento actual y posteriores a la creación de la bicicleta
        reservasDest = self.aDestino.filter(
            fechaFin__gt=fechaCreacion, fechaFin__lte=fecha, estado__in=['pagada', 'cancelada'])
        reservasOrig = self.aOrigen.filter(
            fechaInicio__gt=fechaCreacion, fechaInicio__lte=fecha, estado__in=['pagada', 'cancelada'])

        reservas = reservasDest | reservasOrig
        reservas = reservas.order_by('-fechaFin')

        # Si no hay reservas anteriores no está libre
        if not reservas:
            return False

        # Si hay reservas anteriores, si la última es destino ocupado
        últimaReserva = reservas.first()
        if últimaReserva.ancDestino == self:
            return False

        # Si la utlima previa es origen y no hay reservas después que sea destino está libre
        reservasDestPost = self.aDestino.filter(
            fechaFin__gte=fecha, estado__in=['pagada', 'cancelada'])
        if not reservasDestPost:
            return True

        return False

    def anclajeDisponibleRecogida(self, fecha):
        """
            Obtiene si un anclaje dispone de una bicicleta para una reserva en la fecha y hora indicadas.

            ARGS:
                fecha: fecha que se desea conocer disponibilidad

            RETURN:
                bool: True si dispone de bicicleta y False en caso contrario
        """

        # Si el anclaje está implicado en alguna reserva pendiente de pago no lo usamos
        rDest = self.aDestino.filter(estado='pendiente')
        rOrig = self.aOrigen.filter(estado='pendiente')
        if rDest or rOrig:
            return False

        # Primero miramos si se ha asignado una bicicleta inicial en ese anclaje
        bicis = Bicicleta.objects.filter(anclajeInicio=self).order_by('-fecha')

        # Si ninguna bicicleta fue asignada inicialmente al anclaje
        if not bicis:
            # Obtenemos las reservas anteriores a la hora actual en las que el anclaje es origen o destino
            reservasDest = self.aDestino.filter(
                fechaFin__lte=fecha, estado__in=['pagada', 'cancelada'])
            reservasOrig = self.aOrigen.filter(
                fechaInicio__lte=fecha, estado__in=['pagada', 'cancelada'])

            reservas = reservasDest | reservasOrig
            reservas = reservas.order_by('-fechaFin')

            # Si no hay reservas no hay bicicleta
            if not reservas:
                return False

            # Si hay reservas anteriores
            últimaReserva = reservas.first()

            # Si la última es origen, no hay bicicleta
            if últimaReserva.ancOrigen == self:
                return False

            # Si la última previa es destino y no hay reservas después que sea origen hay bicicleta
            reservasOrigPost = self.aOrigen.filter(
                fechaInicio__gte=fecha, estado__in=['pagada', 'cancelada'])
            if not reservasOrigPost:
                return True

            return False

        # Si hay bicicletas que tienen este anclaje como inicial
        # Obtenemos la bicicleta asignada más recientemente
        bici = bicis.first()
        fechaCreacion = bici.fecha

        # Buscamos reservas anteriores al momento actual
        reservasDest = self.aDestino.filter(
            fechaFin__gt=fechaCreacion, fechaFin__lte=fecha, estado__in=['pagada', 'cancelada'])
        reservasOrig = self.aOrigen.filter(
            fechaInicio__gt=fechaCreacion, fechaInicio__lt=fecha, estado__in=['pagada', 'cancelada'])

        reservas = reservasDest | reservasOrig
        reservas = reservas.order_by('-fechaFin')

        # Si no hay reservas y no hay reservas después que sea origen hay bicicleta
        if not reservas:
            reservasOrigPost = self.aOrigen.filter(
                fechaInicio__gte=fecha, estado__in=['pagada', 'cancelada'])
            if not reservasOrigPost:
                return True

            return False

        # Si hay reservas anteriores
        últimaReserva = reservas.first()

        # Si la última es origen, no hay bicicleta
        if últimaReserva.ancOrigen == self:
            return False

        # Si la última previa es destino y no hay reservas después que sea origen hay bicicleta
        reservasOrigPost = self.aOrigen.filter(
            fechaInicio__gte=fecha, estado__in=['pagada', 'cancelada'])
        if not reservasOrigPost:
            return True

        return False

    def seleccionarBicicleta(self, fechaInicio):
        """
            Obtiene la bicicleta a utilizar en la reserva a partir de la fecha y hora de inicio.

            ARGS:
                fechaInicio: fecha de inicio de la reserva

            RETURN:
                Bicicleta: bicicleta de la reserva
                None: si no dispone de bicicleta
        """

        # Primero miramos si se ha asignado una bicicleta inicial en ese anclaje
        bicis = Bicicleta.objects.filter(anclajeInicio=self).order_by('-fecha')

        if not bicis:
            # Obtenemos la última reserva destino previo a la hora de inicio para obtener la bicicleta
            reservasDest = self.aDestino.filter(fechaFin__lt=fechaInicio, estado__in=[
                                                'pagada', 'cancelada']).first()
            return reservasDest.bicicleta

        # Si hay bicicletas que tienen este anclaje como inicial
        # Obtenemos la bicicleta asignada más recientemente
        bici = bicis.first()
        fechaCreacion = bici.fecha

        # Buscamos reservas con el anclaje como origen anteriores al momento actual y posteriores a la creación de la bicicleta
        reservasOrig = self.aOrigen.filter(
            fechaInicio__gt=fechaCreacion, fechaInicio__lt=fechaInicio, estado__in=['pagada', 'cancelada'])

        # Si no ha habido reservas, devuelvo última bicicleta asignada
        if not reservasOrig:
            return bici

        # Si hay reservas con anclaje como origen
        # Obtenemos la última reserva destino previo a la hora de inicio para obtener la bicicleta
        reservasDest = self.aDestino.filter(
            fechaFin__gt=fechaCreacion, fechaFin__lt=fechaInicio, estado__in=['pagada', 'cancelada']).first()
        return reservasDest.bicicleta


class Bicicleta(models.Model):
    """
        Modelo de una bicicleta del campus
    """

    # Anclaje inicial en el que se ubica la bicicleta
    anclajeInicio = models.ForeignKey(Anclaje,
                                      on_delete=models.PROTECT)

    # Estación inicial en la que se ubica la bicicleta
    estacionInicial = models.ForeignKey(Estacion,
                                        on_delete=models.PROTECT)

    # Fecha de creación
    fecha = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return f"Bicicleta ubicada inicialmente en el anclaje número {self.anclajeInicio.numAnclaje} de la estación {self.estacionInicial.nombre}"

    def anclajeBicicleta(self):
        """
            Obtiene el anclaje en el que se encuentra la bicicleta actualmente.

            RETURN:
                Anclaje: anclaje asociado
                None: está en uso actualmente
        """
        reserva = self.biciReservas.filter(bicicleta=self, fechaInicio__lte=timezone.localtime(
        ), estado__in=['pagada', 'cancelada']).order_by('-fechaInicio').first()
        if not reserva:
            return self.anclajeInicio

        if reserva.fechaFin <= timezone.localtime():
            return reserva.ancDestino

        return None


class Tarifa(models.Model):
    """
        Modelo de una tarifa del servicio
    """

    # Importe de la tarifa
    importe = models.FloatField(default=0.0)

    # Precio por minuto de la reserva de una bicicleta
    precioMinuto = models.FloatField(default=0.0)

    # Breve descripción de la tarifa
    descripcion = models.CharField(max_length=1024)

    # Opciones de tarifa posibles
    tiempo = [
        ('mensual', 'Mensual'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]

    # Duración de la tarifa
    duracion = models.CharField(
        max_length=20,
        choices=tiempo,
        default='mensual',
        blank=False,
        unique=True
    )

    def __str__(self):
        return f"Duración de la tarifa: {self.duracion}. Importe: {self.importe} - Precio por minuto: {self.precioMinuto}"

    def getDuracion(self):
        """
            Obtiene la duración de la tarifa.

            RETURN:
                str: duración de la tarifa
        """
        return self.duracion

    def obtenerImporte(self):
        """
            Obtiene el importe de la tarifa.

            RETURN:
                Float: importe de la tarifa
        """
        return round(self.importe, 2)

    def actualizarImporte(self, importe):
        """
            Actualiza el importe de la tarifa.

            ARGS:
                importe: nuevo importe deseado

            RETURN:
                bool: True en caso de que se actualice el importe correctamente o False en caso contrario

        """

        if importe <= 0:
            return False

        # Actualización del importe
        self.importe = round(importe, 2)
        self.save()
        return True

    def actualizarPrecioMinuto(self, precioMinuto):
        """
            Actualiza el precio por minuto de la tarifa
            en caso de que la tarifa no sea mensual.

            ARGS:
                precioMinuto: nuevo precio por minuto deseado

            RETURN:
                bool: True en caso de que se actualice el precio por minuto correctamente o False en caso contrario

        """

        if precioMinuto <= 0:
            return False

        # Verificar que la tarifa no es mensual
        if self.duracion == "mensual":
            return False

        # Actualización precio por minuto
        self.precioMinuto = round(precioMinuto, 2)
        self.save()
        return True

    def calcularFechaFin(self, inicio):
        """
            Calcula la fecha fin de un contrato a partir de la tarifa
            y la fecha de inicio.

            ARGS:
                inicio: fecha de inicio

            RETURN:
                date: fecha fin del contrato

        """
        # En función de la duración de la tarifa devuelve la fecha correcta
        if self.duracion == "mensual":
            fin = inicio + relativedelta(days=29)
        elif self.duracion == "semestral":
            fin = inicio + relativedelta(days=180-1)
        else:
            fin = inicio + relativedelta(days=360-1)

        return fin

    def calcularPrecioReservaTarifa(self, fechaInicio, fechaFin):
        """
            Determina el importe de una reserva en función de su duración.

            ARGS:
                fechaInicio: fecha de inicio de la reserva deseada
                fechaFin: fecha de fin de la reserva deseada

            RETURN:
                float: importe de la reserva
        """

        if fechaFin < fechaInicio:
            return -1
        minutos_totales = fechaFin - fechaInicio
        minutos_totales = floor(minutos_totales.total_seconds() / 60)
        return round(minutos_totales*self.precioMinuto, 2)


class Contrato(models.Model):
    """
        Modelo de un contrato
    """

    # Fecha de inicio
    inicio = models.DateField()

    # Fecha de fin
    fin = models.DateField()

    # Usuario del contrato
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='contratos'
    )

    # Tarifa del contrato
    tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"Inicio: {self.inicio} - Fin: {self.fin} - Usuario: {self.usuario.usuario.username} - Tarifa: {self.tarifa.duracion}"

    def getFin(self):
        """
            Obtiene la fecha fin del contrato.

            RETURN:
                date: fecha fin del contrato

        """
        return self.fin


class Notificacion(models.Model):
    """
        Modelo de una notificación de un usuario
    """

    # Fecha de envío
    fecha = models.DateField()

    # Contenido del mensaje
    msg = models.CharField(max_length=2048)

    # Usuario asociado a la notificación
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )

    # Bool para saber si ha sido leída
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fecha}: {self.msg}"

    def notificacionLeida(self):
        """
            Permite conocer si la notificación ha sido leída por el usuario

            RETURN:
                bool: True en caso de que la notificación haya sido leída o False en caso contrario

        """
        return self.leida

    def leer(self):
        """
            Acción de lectura de una notificación.
        """

        # Actualización campo leida
        self.leida = True
        self.save()


class UsuarioPendiente(models.Model):
    """
        Modelo de un nuevo usuario del sistema que se almacena
        temporalmente hasta que realice el pago.
    """

    # Nombre de usuario
    usuario = models.CharField(max_length=32, unique=True)

    # Nombre
    nombre = models.CharField(max_length=100)

    # Apellidos
    apellidos = models.CharField(max_length=150)

    # Contraseña
    contraseña = models.CharField(max_length=255)

    # Teléfono
    tlf = models.CharField(
        max_length=9,
        validators=[RegexValidator(
            r'^\d{9}$', 'El teléfono debe tener 9 dígitos exactos')]
    )

    # Tarifa deseada
    tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.PROTECT
    )

    # Fecha de expiración del usuario si no paga antes
    expires_at = models.DateTimeField()


# Métodos genéricos del sistema

def usuarioExistente(usuario):
    """
        Verifica que el nombre de usuario no exista.

        ARGS:
            usuario: nombre de usuario

        RETURN:
            bool: True en caso de que exista o False en caso contrario

    """

    user = UsuarioSistema.objects.filter(username=usuario)
    return len(user) != 0


def getUsuarioSistemaByName(usuario):
    """
        Obtiene un usuario del sistema a partir de su nombre de usuario

        ARGS:
            usuario: nombre de usuario

        RETURN:
            UsuarioSistema: instancia del usuario del sistema
            None: si no existe dicho usuario

    """
    return UsuarioSistema.objects.filter(username=usuario).first()


def getTarifaByName(nombre):
    """
        Obtiene una tarifa del sistema a partir de su duración

        ARGS:
            nombre: duración de la tarifa

        RETURN:
            Tarifa: instancia de la tarifa del sistema
            None: si no existe dicha tarifa

    """
    return Tarifa.objects.filter(duracion=nombre).first()


def getEstacionByName(nombre):
    """
        Obtiene una estación del sistema a partir de su nombre

        ARGS:
            nombre: nombre de la estación

        RETURN:
            Estación: instancia de la estación del sistema
            None: si no existe dicha estación

    """
    return Estacion.objects.filter(nombre=nombre).first()


def getAnclajeByID(anclajeId):
    """
        Obtiene un anclaje del sistema a partir de su id

        ARGS:
            anclajeId: id del anclaje

        RETURN:
            Anclaje: instancia del anclaje del sistema
            None: si no existe dicho anclaje

    """
    return Anclaje.objects.filter(id=anclajeId).first()


def getBicicletaByID(bicicletaId):
    """
        Obtiene una bicicleta del sistema a partir de su id

        ARGS:
            bicicletaId: id de la bicicleta

        RETURN:
            Bicicleta: instancia de la bicicleta del sistema
            None: si no existe dicha bicicleta

    """
    return Bicicleta.objects.filter(id=bicicletaId).first()
