from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sgu_sgs.models import Gestor, Notificacion, UsuarioSistema, UsuarioPendiente, Usuario, usuarioExistente, getUsuarioSistemaByName, getTarifaByName
from sgu_sgs.serializers import NotificacionSerializer, UsuarioPendienteSerializer
from django.contrib.auth.hashers import make_password
from pagosPayPal.paypal import PayPal
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from datetime import timedelta
from django.db import transaction, IntegrityError

# SGU


class CrearCuentaUsuarioAPIView (APIView):
    """
    APIView para crear una nueva cuenta de usuario mediante el envío de los datos solicitados y
    proceder a realizar el pago.
    """
    permission_classes = []

    def post(self, request):
        # Eliminación usuarios pendientes expirados
        UsuarioPendiente.objects.filter(
            expires_at__lt=timezone.localtime()
        ).delete()

        # Validación campos recibidos para crear el nuevo usuario
        serializer = UsuarioPendienteSerializer(data=request.data)
        if not serializer.is_valid():
            data = {"Mensaje": "Los campos introducidos no son correctos.",
                    "errores": serializer.errors}
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Creación del usuario temporal hasta que realice el pago de la cuota de uso
        try:
            with transaction.atomic():
                usuarioPendiente = UsuarioPendiente.objects.create(
                    usuario=serializer.validated_data["usuario"],
                    nombre=serializer.validated_data["nombre"],
                    apellidos=serializer.validated_data["apellidos"],
                    contraseña=make_password(
                        serializer.validated_data["contraseña"]),
                    tlf=serializer.validated_data["tlf"],
                    tarifa=serializer.validated_data["tarifa"],
                    expires_at=timezone.localtime() + timedelta(minutes=10))
        except IntegrityError:
            return Response(
                {"Mensaje": "El nombre de usuario ya existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención importe y fecha de inicio del contrato
        importe = serializer.validated_data["tarifa"].obtenerImporte()
        fin = serializer.validated_data["tarifa"].calcularFechaFin(
            timezone.localtime().date())

        # Creación y devolución de la orden de pago al frontend para proceder al pago de la cuota de uso
        response = PayPal.crear_orden(importe)
        if response.status_code != status.HTTP_201_CREATED:
            return response

        return Response({"order_id": response.data.get("order_id"), "user_id": usuarioPendiente.id, "importe": importe, "fin": str(fin)}, status=status.HTTP_201_CREATED)


class PagarAltaUsuarioAPIView (APIView):
    """
    APIView para realizar la captura del pago, verificar el estado del pago y crear el nuevo usuario para que
    pueda acceder a la aplicación y hacer uso del servicio.
    """
    permission_classes = []

    def post(self, request):

        # Obtención y validación datos de entrada
        order_id = request.data.get("order_id")
        user_id = request.data.get("user_id")
        if order_id is None:
            return Response(
                {"Mensaje": "No se ha recibido order id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_id is None:
            return Response(
                {"Mensaje": "No se ha recibido user id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Capturar orden de pago para conocer estado del pago
        response = PayPal.capturar_orden(order_id)

        if response.status_code != status.HTTP_201_CREATED and response.status_code != status.HTTP_200_OK:
            return Response(response.data, status=response.status_code)

        # En caso éxitoso, buscamos el usuario pendiente de creación a partir del user_id recibido y creamos el nuevo usuario
        user = UsuarioPendiente.objects.filter(id=user_id).first()
        if user is None:
            return Response(
                {"Mensaje": "User id no encontrado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuarioSistema = UsuarioSistema.objects.create(
            username=user.usuario, password=user.contraseña, rol="usuario")

        nuevoUsuario = Usuario.objects.create(
            usuario=usuarioSistema, nombre=user.nombre, apellidos=user.apellidos, saldo=0.0, tlf=user.tlf)
        nuevoUsuario.crearContrato(user.tarifa)

        # Borramos el usuario pendiente creado anteriormente
        user.delete()
        return Response(
            {"Mensaje": "Usuario creado con éxito."},
            status=status.HTTP_200_OK
        )


class AltaGestorAPIView (APIView):
    """
    APIView para crear un nuevo gestor en el sistema.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "administrador":
            return Response(
                {"Mensaje": "Debes ser un administrador."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        nombre = request.data.get("nombre")
        apellidos = request.data.get("apellidos")
        usuario = request.data.get("usuario")
        contra = request.data.get("contraseña")

        if nombre is None or nombre == "" or apellidos is None or apellidos == "" or usuario is None or usuario == "" or contra is None or contra == "":
            return Response(
                {"Mensaje": "Debe completar todos los campos necesarios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el nombre de usuario no exista
        if usuarioExistente(usuario):
            return Response(
                {"Mensaje": "Error al crear el gestor. Nombre de usuario ya existente"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar contraseña
        try:
            validate_password(contra)
        except ValidationError:
            return Response(
                {"Mensaje": "Error al crear el gestor. Contraseña poco segura"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Creación nuevo gestor
        usuarioSistema = UsuarioSistema(username=usuario, rol="gestor")

        usuarioSistema.set_password(contra)
        usuarioSistema.save()

        gestor = Gestor(usuario=usuarioSistema,
                        nombre=nombre, apellidos=apellidos)
        gestor.save()

        return Response(
            {"Mensaje": f"Gestor {usuario} creado con éxito."},
            status=status.HTTP_200_OK
        )


class BajaGestorAPIView (APIView):
    """
    APIView para dar de baja un gestor existente en el sistema.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "administrador":
            return Response(
                {"Mensaje": "Debes ser un administrador."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        usuario = request.data.get("usuario")

        if usuario is None:
            return Response(
                {"Mensaje": "Debe indicar el gestor a borrar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención gestor que se desea borrar a partir del nombre de usuario
        usuarioSistema = getUsuarioSistemaByName(usuario)
        if usuarioSistema is None:
            return Response(
                {"Mensaje": "Error al borrar el gestor. Gestor no existente"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el usuario es un gestor
        if usuarioSistema.getRol() != "gestor":
            return Response(
                {"Mensaje": "Error al borrar el gestor. Gestor no existente"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Borrar gestor
        usuarioSistema.delete()

        return Response(
            {"Mensaje": f"Gestor {usuario} borrado con éxito."},
            status=status.HTTP_200_OK
        )


class ConsultarPerfilAPIView (APIView):
    """
    APIView para consultar el perfil asociado a un usuario del sistema.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "usuario":
            return Response(
                {"Mensaje": "Debes ser un usuario."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtener instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Obtener datos asociados al perfil del usuario
        data = usuario.getPerfil()
        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ModificarPerfilAPIView (APIView):
    """
    APIView para modificar los datos asociados al perfil de un usuario del sistema.
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
        tlf = request.data.get("tlf")

        if tlf is None:
            return Response(
                {"Mensaje": "Debe indicar el número de teléfono."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Modificar el número de teléfono del usuario
        if usuario.modificarPerfil(tlf) is False:
            return Response(
                {"Mensaje": "Error al modificar el perfil. Número de teléfono erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"Mensaje": "Datos actualizados correctamente."},
            status=status.HTTP_200_OK
        )


class RenovarContratoAPIView (APIView):
    """
    APIView para realizar la renovación del contrato indicando la nueva cuota de uso.
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
        tarifa = request.data.get("tarifa")

        if tarifa is None:
            return Response(
                {"Mensaje": "Debe indicar la tarifa que desea contratar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Obtener nueva tarifa deseada
        t = getTarifaByName(tarifa.lower())
        if t is None:
            return Response(
                {"Mensaje": "Debe indicar una tarifa válida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calcular fecha inicio y fin del contrato e importe del pago
        importe = t.obtenerImporte()
        inicio = usuario.getFechaInicioContrato()
        fin = usuario.calcularFechaFinContrato(inicio, t)

        # Creación y devolución de la orden de pago para proceder al pago de la renovación
        response = PayPal.crear_orden(importe)
        if response.status_code != status.HTTP_201_CREATED:
            return response

        return Response({"order_id": response.data.get("order_id"), "user_id": user.id, "importe": importe, "fin": str(fin)}, status=status.HTTP_201_CREATED)


class PagarRenovacionContratoAPIView (APIView):
    """
    APIView para realizar la captura del pago de la renovación del contrato, consultar el estado del pago
    y crear un nuevo contrato en caso de éxito ampliando la duración de acceso al servicio.
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
        user_id = request.data.get("user_id")
        tarifa = request.data.get("tarifa")

        if tarifa is None:
            return Response(
                {"Mensaje": "Debe indicar la tarifa que desea contratar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order_id is None:
            return Response(
                {"Mensaje": "No se ha recibido order id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_id is None:
            return Response(
                {"Mensaje": "No se ha recibido user id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención nueva tarifa deseada
        t = getTarifaByName(tarifa.lower())
        if t is None:
            return Response(
                {"Mensaje": "Debe indicar una tarifa válida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Capturar orden del pago para conocer estado del pago
        response = PayPal.capturar_orden(order_id)

        if response.status_code != status.HTTP_201_CREATED and response.status_code != status.HTTP_200_OK:
            return Response(response.data, status=response.status_code)

        # Si el pago se realizó correctamente
        user = UsuarioSistema.objects.filter(id=user_id).first()
        if user is None:
            return Response(
                {"Mensaje": "User id no encontrado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtenemos instancia completa del usuario
        user = user.obtenerPerfilCompleto()

        # Renovamos contrato
        user.renovarContrato(t)

        return Response(
            {"Mensaje": "Contrato renovado con éxito."},
            status=status.HTTP_200_OK
        )


class LeerNotificacionesAPIView (APIView):
    """
    APIView para leer las notificaciones enviadas al usuario que aún no ha leído.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "usuario":
            return Response(
                {"Mensaje": "Debes ser un usuario."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtenemos instancia completa del usuario
        usuario = user.obtenerPerfilCompleto()

        # Comprobamos si es necesario enviar notificación de aviso de fin de contrato
        usuario.avisarExpiracionContrato()

        # Obtenemos todas las notificaciones del usuario
        noti = Notificacion.objects.filter(
            usuario=usuario).order_by('-fecha')
        notificaciones = []
        for n in noti:

            # Si la notificación no ha sido leída, se lee y se muestra al usuario
            if n.notificacionLeida() is False:
                n.leer()
                notificaciones.append(n)

        # Devuelve las notificaciones serializadas al frontend
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
