from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sgr.models import Reserva
from sgu_sgs.models import getEstacionByName, getUsuarioSistemaByName
from django.utils.dateparse import parse_date, parse_time
from pagosPayPal.paypal import PayPal
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from sgr.serializers import ReservaSerializer
from django.db import transaction
# SGR


class HacerReservaAPIView (APIView):
    """
    APIView para realizar una reserva.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "usuario":
            return Response(
                {"Mensaje": "Debes ser un usuario."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Eliminación automática de reservas expiradas
        Reserva.objects.filter(
            estado='pendiente',
            expires_at__lt=timezone.localtime()
        ).delete()

        # Obtención y validación datos de entrada
        inicio = request.data.get("inicio")
        fin = request.data.get("fin")
        horaInicio = request.data.get("horaInicio")
        horaFin = request.data.get("horaFin")
        origen = request.data.get("origen")
        destino = request.data.get("destino")

        if inicio is None or inicio == "" or fin is None or fin == "" or horaInicio is None or horaInicio == "" or horaFin is None or horaFin == "" or origen is None or origen == "" or destino is None or destino == "":
            return Response(
                {"Mensaje": "Debe indicar todos los campos necesarios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Obtención estaciones
        estOrigen = getEstacionByName(origen)
        if estOrigen is None:
            return Response(
                {"Mensaje": "Estación origen no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        estDestino = getEstacionByName(destino)
        if estDestino is None:
            return Response(
                {"Mensaje": "Estación destino no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención fecha y hora de inicio y fin
        inicio = parse_date(inicio)
        fin = parse_date(fin)
        if not inicio or not fin:
            return Response(
                {"Mensaje": "Formato de fecha incorrecto. Usa YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        horaInicio = parse_time(horaInicio)
        horaFin = parse_time(horaFin)
        if not horaInicio or not horaFin:
            return Response(
                {"Mensaje": "Formato de hora incorrecto. Usa horas:minutos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificamos que el usuario tenga contrato
        contrato = usuario.getContratoActual()
        if contrato is None:
            return Response(
                {"Mensaje": "Debes disponer de un contrato activo para realizar reservas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificamos que la reserva es posterior al momento actual y son coherentes
        fecha_hora = datetime.combine(inicio, horaInicio)
        fecha_hora_inicio = timezone.make_aware(fecha_hora)
        fecha_hora = datetime.combine(fin, horaFin)
        fecha_hora_fin = timezone.make_aware(fecha_hora)
        ahora = timezone.localtime()

        if fecha_hora_inicio < ahora or fecha_hora_fin < ahora:
            return Response(
                {"Mensaje": "Debes introducir fechas posteriores al momento actual."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if fecha_hora_inicio > fecha_hora_fin:
            return Response(
                {"Mensaje": "La fecha de inicio debe ser anterior a la de fin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificamos que no haga la reserva fuera del periodo del contrato
        if inicio > contrato.fin or inicio < contrato.inicio or fin < contrato.inicio or fin > contrato.fin:
            return Response(
                {"Mensaje": "Debes realizar la reserva en el periodo de tu contrato activo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificamos la viabilidad de la reserva
        if not usuario.reservaPosible(fecha_hora_inicio, fecha_hora_fin):
            return Response(
                {"Mensaje": "Ya dispones de una reserva en esa franja horaria."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculamos precio de la reserva
        importe = usuario.calcularPrecioReservaUsuario(
            fecha_hora_inicio, fecha_hora_fin)
        importeFinal = usuario.precioReservaSaldo(importe)

        
        with transaction.atomic():
            anclajesOrigen = estOrigen.anclajes.select_for_update()
            anclajesDestino = estDestino.anclajes.select_for_update()

            # Seleccionamos anclaje de origen y destino
            ancOrigen = estOrigen.seleccionarAnclajeOrigen(fecha_hora_inicio)

            if estOrigen == estDestino:
                ancDestino = ancOrigen
            else:
                ancDestino = estDestino.seleccionarAnclajeDestino(fecha_hora_fin)

            if not ancOrigen or not ancDestino:
                return Response(
                    {"Mensaje": "No es posible realizar una reserva con las condiciones deseadas."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Seleccionamos bicicleta
            bicicleta = ancOrigen.seleccionarBicicleta(fecha_hora_inicio)

            # Creamos la reserva con estado pendiente de pago para reservar franja horaria
            r = Reserva.objects.create(fechaInicio=fecha_hora_inicio, fechaFin=fecha_hora_fin, importe=importeFinal, estado='pendiente', estOrigen=estOrigen,
                                    estDestino=estDestino, ancOrigen=ancOrigen, ancDestino=ancDestino, bicicleta=bicicleta, usuario=usuario, expires_at=timezone.localtime() + timedelta(minutes=10))

        # Si el importe es 0, creamos la reserva automáticamente
        if importeFinal == 0:
            r.actualizarEstado('pagada')
            r.notificarReserva()

            # Descontamos saldo al usuario
            usuario.actualizarSaldo(importeFinal-importe)

            return Response(
                {"Mensaje": "Reserva realizada con éxito.",
                    "importe": importeFinal, "reserva_id": r.id},
                status=status.HTTP_200_OK
            )

        # Creación y devolución de la orden de pago para proceder al pago de la reserva
        response = PayPal.crear_orden(importe)
        if response.status_code != status.HTTP_201_CREATED:
            return response

        return Response({"order_id": response.data.get("order_id"), "reserva_id": r.id, "importe": importeFinal, "saldo": importeFinal-importe, "inicio": str(inicio), "horaInicio": str(horaInicio), "horaFin": str(horaFin), "fin": str(fin), "origen": estOrigen.nombre, "destino": estDestino.nombre}, status=status.HTTP_201_CREATED)


class PagarReservaAPIView (APIView):
    """
        APIView para realizar la captura del pago, verificar el estado del pago y cambiar el estado de la reserva a pagada.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "usuario":
            return Response(
                {"Mensaje": "Debes ser un usuario."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        order_id = request.data.get("order_id")
        reserva_id = request.data.get("reserva_id")
        saldo = request.data.get("saldo")

        if order_id is None:
            return Response(
                {"Mensaje": "No se ha recibido order id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reserva_id is None:
            return Response(
                {"Mensaje": "No se ha recibido reserva id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reserva_id = int(reserva_id)
        except Exception:
            return Response(
                {"Mensaje": "Reserva id con formato erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if saldo is None:
            return Response(
                {"Mensaje": "No se ha recibido saldo a descontar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            saldo = float(saldo)
        except Exception:
            return Response(
                {"Mensaje": "Saldo con formato erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Instancia de la reserva a pagar
        r = Reserva.objects.filter(
            id=reserva_id, estado='pendiente'
        ).first()

        # Si la reserva no existe, error
        if r is None:
            return Response(
                {"Mensaje": "Reserva no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si la reserva ha expirado se cancela el pago
        if r.expires_at <= timezone.localtime():
            return Response(
                {"Mensaje": "Reserva expirada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Capturar orden del pago para conocer estado del pago
        response = PayPal.capturar_orden(order_id)

        if response.status_code != status.HTTP_201_CREATED and response.status_code != status.HTTP_200_OK:
            return Response(response.data, status=response.status_code)

        # Si el pago se realizó correctamente, actualizamos estado de la reserva y notificamos
        r.actualizarEstado('pagada')
        r.notificarReserva()

        # Descontamos saldo al usuario
        usuario = user.obtenerPerfilCompleto()
        usuario.actualizarSaldo(saldo)

        return Response(
            {"Mensaje": "Reserva realizada con éxito."},
            status=status.HTTP_200_OK
        )


class CancelarReservaAPIView (APIView):
    """
    APIView para cancelar una reserva.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "usuario":
            return Response(
                {"Mensaje": "Debes ser un usuario."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        reserva_id = request.data.get("reserva_id")

        if reserva_id is None:
            return Response(
                {"Mensaje": "No se ha recibido reserva id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reserva_id = int(reserva_id)
        except Exception:
            return Response(
                {"Mensaje": "Reserva id con formato erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Instancia de la reserva a cancelar
        r = usuario.getReservaById(reserva_id)

        # Si la reserva no existe, error
        if r is None:
            return Response(
                {"Mensaje": "Reserva no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si la reserva no está pagada, error
        if r.estado == 'pendiente':
            return Response(
                {"Mensaje": "Reserva no pagada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vemos si la reserva es cancelable
        if not r.esCancelable():
            return Response(
                {"Mensaje": "Reserva no cancelable."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Cancelamos la reserva
        r.cancelar()

        return Response(
            {"Mensaje": "Reserva cancelada con éxito."},
            status=status.HTTP_200_OK
        )


class ConsultarReservasAPIView (APIView):
    """
    APIView para consultar reservas de un usuario o de todos en función del rol.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        rol = user.getRol()
        if rol == "administrador":
            return Response(
                {"Mensaje": "No tienes permisos para ver las reservas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtenemos reservas
        if rol == 'usuario':
            # Si es usuario solo sus reservas
            usuario = user.obtenerPerfilCompleto()
            reservas = usuario.getReservas()
        else:
            # Si es gestor todas las reservas
            reservas = Reserva.objects.filter(
                estado__in=['pagada', 'cancelada']).order_by('-fechaInicio')

        # Devuelve todas las reservas del sistema serializadas al frontend
        reservas.order_by('-fechaInicio')
        serializer = ReservaSerializer(reservas, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ConsultarReservasFiltrosAPIView (APIView):
    """
    APIView para filtrar las reservas de la aplicación y obtener únicamente
    aquellas que cumplan las condiciones indicadas.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        rol = user.getRol()
        if rol == "administrador":
            return Response(
                {"Mensaje": "No tienes permiso para consultar las reservas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        inicio = request.data.get("inicio")
        fin = request.data.get("fin")
        origen = request.data.get("origen")
        destino = request.data.get("destino")
        usuario = request.data.get("usuario")

        # Obtención criterios indicados para filtrar las reservas
        # Fecha de inicio que se desea filtrar

        if inicio is not None:
            inicio = parse_date(inicio)
            if not inicio:
                return Response(
                    {"Mensaje": "Formato de fecha incorrecto. Usa YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Filtrar reservas a partir de la fecha de inicio indicada
            r1 = Reserva.objects.filter(fechaInicio__date__gte=inicio)
        else:
            r1 = Reserva.objects.all()

        # Fecha fin que se desea filtrar
        if fin is not None:
            fin = parse_date(fin)
            if not fin:
                return Response(
                    {"Mensaje": "Formato de fecha incorrecto. Usa YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Filtrar reservas a partir de la fecha fin indicada
            r2 = Reserva.objects.filter(fechaFin__date__lte=fin)
        else:
            r2 = Reserva.objects.all()

        # Estación de origen que se desea filtrar
        if origen is not None:
            o = getEstacionByName(origen)
            if o is None:
                return Response(
                    {"Mensaje": "Debe indicar una estación válida."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Filtrar reservas a partir de la estación de origen
            r3 = Reserva.objects.filter(estOrigen=o)
        else:
            r3 = Reserva.objects.all()

        # Estación de destino que se desea filtrar
        if destino is not None:
            d = getEstacionByName(destino)
            if d is None:
                return Response(
                    {"Mensaje": "Debe indicar una estación válida."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Filtrar reservas a partir de la estación destino
            r4 = Reserva.objects.filter(estDestino=d)
        else:
            r4 = Reserva.objects.all()

        # Intersección de resultados
        reservas = r1 & r2 & r3 & r4

        # Solo las confirmadas, no las pendientes de pago
        reservas = reservas.filter(
            estado__in=['pagada', 'cancelada']).order_by('-fechaInicio')

        # Filtramos reservas por usuario
        if rol == 'usuario':
            usuario = user.obtenerPerfilCompleto()
            reservas = reservas.filter(usuario=usuario)
        else:
            if usuario is not None:
                usuario = getUsuarioSistemaByName(usuario)
                if usuario is None:
                    return Response(
                        {"Mensaje": "Usuario no existente."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if usuario.getRol() != 'usuario':
                    return Response(
                        {"Mensaje": "Debe indicar un usuario existente."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                reservas = reservas.filter(
                    usuario=usuario.obtenerPerfilCompleto())

        # Devuelve las reservas filtradas serializadas al frontend
        serializer = ReservaSerializer(reservas, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
