from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sgu_sgs.models import Tarifa, Gestor, Contrato, Estacion, Bicicleta, getTarifaByName, getEstacionByName, getBicicletaByID
from sgu_sgs.serializers import GestorSerializer, BicicletaSerializer, EstacionSerializer, ContratoSerializer, TarifaSerializer, TarifaListaSerializer
from django.utils.dateparse import parse_date
from decimal import Decimal
from django.utils import timezone

# SGS


class ActualizarTarifaAPIView (APIView):
    """
    APIView para actualizar el importe o precio por minuto de las tarifas existentes.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        nombre = request.data.get("nombre")
        importe = request.data.get("importe")
        precioMinuto = request.data.get("precioMinuto")

        if nombre is None or ((importe is None or importe == "") and (precioMinuto is None or precioMinuto == "")):
            return Response(
                {"Mensaje": "Debe indicar tarifa y nuevo importe o precio por minuto."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención tarifa que se desea actualizar
        tarifa = getTarifaByName(nombre.lower())
        if tarifa is None:
            return Response(
                {"Mensaje": "Debe indicar una tarifa válida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención nuevo importe deseado
        if importe is not None and importe != "":
            try:
                importe = float(importe)

                # Actualización importe
                if tarifa.actualizarImporte(importe) is False:
                    return Response(
                        {"Mensaje": "Error al actualizar el importe de la tarifa."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except ValueError:
                return Response(
                    {"Mensaje": "Importe erróneo."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Obtención nuevo precio por minuto deseado
        if precioMinuto is not None and precioMinuto != "":
            try:
                precioMinuto = float(precioMinuto)

                # Verificación que la tarifa no es mensual. La tarifa mensual no permite actualizar precio por minuto
                if tarifa.getDuracion() == "mensual":
                    return Response(
                        {"Mensaje": "No se puede actualizar el precio por minuto de la tarifa mensual."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Actualización precio por minuto
                if tarifa.actualizarPrecioMinuto(precioMinuto) is False:
                    return Response(
                        {"Mensaje": "Error al actualizar el precio por minuto de la tarifa."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except ValueError:
                return Response(
                    {"Mensaje": "Precio por minuto erróneo."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"Mensaje": "Tarifa actualizada con éxito."},
            status=status.HTTP_200_OK
        )


class ConsultarTarifaAPIView (APIView):
    """
    APIView para consultar la información de cada tarifa existente del servicio.
    """
    permission_classes = []

    def post(self, request):

        # Obtención y validación datos de entrada
        nombre = request.data.get("nombre")

        if nombre is None:
            return Response(
                {"Mensaje": "Debe indicar la tarifa que desea consultar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención tarifa que se desea consultar
        tarifa = getTarifaByName(nombre.lower())
        if tarifa is None:
            return Response(
                {"Mensaje": "Debe indicar una tarifa válida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Devuelve la tarifa serializada al frontend
        serializer = TarifaSerializer(tarifa, many=False)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AltaEstacionAPIView (APIView):
    """
    APIView para realizar el alta de una nueva estación del campus.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        nombre = request.data.get("nombre")
        ubicacion = request.data.get("ubicacion")
        nAnclajes = request.data.get("nAnclajes")
        latitud = request.data.get("latitud")
        longitud = request.data.get("longitud")

        if nombre is None or nombre == "" or ubicacion is None or ubicacion == "" or nAnclajes is None or nAnclajes == "" or latitud is None or latitud == "" or longitud is None or longitud == "":
            return Response(
                {"Mensaje": "Debe indicar todos los campos necesarios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el nombre de la estación es único y no existe
        est = getEstacionByName(nombre)
        if est is not None:
            return Response(
                {"Mensaje": "Nombre de la estación ya existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención número de anclajes deseados para la nueva estación
        try:
            nAnclajes = int(nAnclajes)
            if nAnclajes <= 0:
                return Response(
                    {"Mensaje": "Número de anclajes erróneo."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"Mensaje": "Número de anclajes erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención coordenadas de la estación
        try:
            lat = Decimal(latitud)
            long = Decimal(longitud)
            if lat < -90 or lat > 90 or long < -180 or long > 180:
                return Response(
                    {"Mensaje": "Coordenadas no existentes."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return Response(
                {"Mensaje": "Coordenadas erróneas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Creación nueva estación
        estacion = Estacion.objects.create(
            nombre=nombre, ubicacion=ubicacion, latitud=lat, longitud=long,  nAnclajes=nAnclajes)
        estacion.crearAnclajes()

        return Response(
            {"Mensaje": f"Estación {nombre} creada con éxito."},
            status=status.HTTP_200_OK
        )


class AltaBicicletaAPIView (APIView):
    """
    APIView para realizar el alta de una nueva bicicleta del campus.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        estacion = request.data.get("estacion")
        anclajeId = request.data.get("anclajeId")

        if estacion is None or anclajeId is None:
            return Response(
                {"Mensaje": "Debe indicar todos los campos necesarios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que la estación donde se desea ubicar la bicicleta existe
        est = getEstacionByName(estacion)
        if est is None:
            return Response(
                {"Mensaje": "Estacion no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención número de anclaje donde ubicar la bicicleta
        try:
            anclajeId = int(anclajeId)
            if anclajeId < 1:
                return Response(
                    {"Mensaje": "Número de anclaje erróneo."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"Mensaje": "Número de anclaje erróneo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención anclaje donde ubicar la bicicleta
        anclaje = est.getAnclajeByNumAnclaje(anclajeId)

        if anclaje is None:
            return Response(
                {"Mensaje": f"Anclaje con número {anclajeId} no existente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el anclaje está libre para asignar
        if anclaje.anclajeDisponibleAsignacion(timezone.localtime()) is False:
            return Response(
                {"Mensaje": f"Anclaje {anclajeId} de la estacion {est.nombre} ocupado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear bicicleta
        Bicicleta.objects.create(anclajeInicio=anclaje, estacionInicial=est)

        return Response(
            {"Mensaje": "Bicicleta creada con éxito."},
            status=status.HTTP_200_OK
        )


class ConsultarEstadoCampusAPIView (APIView):
    """
    APIView para consultar el estado actual del campus indicando número de
    bicicletas y anclajes disponibles.
    """
    permission_classes = []

    def post(self, request):

        # Obtención y validación datos de entrada
        estacion = request.data.get("estacion")

        if estacion is None:
            return Response(
                {"Mensaje": "Debe indicar la estacion."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención de la estación de la que se desea consultar el estado
        est = getEstacionByName(estacion)
        if est is None:
            return Response(
                {"Mensaje": "Estacion no encontrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención número de anclajes y bicicletas disponibles en la estación seleccionada
        data = est.getDisponibilidadAnclajeBicicleta()
        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ConsultarContratosAPIView (APIView):
    """
    APIView para consultar los contratos existentes de la aplicación.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Devuelve todos los contratos del sistema serializados al frontend
        serializer = ContratoSerializer(
            Contrato.objects.all().order_by('-inicio'), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ConsultarContratosFiltrosAPIView (APIView):
    """
    APIView para filtrar los contratos de la aplicación y obtener únicamente
    aquellos que cumplan las condiciones indicadas.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        inicio = request.data.get("inicio")
        fin = request.data.get("fin")
        tarifa = request.data.get("tarifa")

        # Obtención criterios indicados para filtrar los contratos
        # Tarifa que se desea filtrar
        if tarifa is not None:
            t = getTarifaByName(tarifa.lower())
            if t is None:
                return Response(
                    {"Mensaje": "Debe indicar una tarifa válida."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Filtrar contratos a partir de la tarifa deseada
            c1 = Contrato.objects.filter(tarifa=t)
        else:
            c1 = Contrato.objects.all()

        # Fecha inicio para filtrar
        if inicio is not None:
            inicio = parse_date(inicio)
            if not inicio:
                return Response(
                    {"Mensaje": "Formato de fecha incorrecto. Usa YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Filtrar contratos a partir de la fecha de inicio indicada
            c2 = Contrato.objects.filter(inicio__gte=inicio)
        else:
            c2 = Contrato.objects.all()

        # Fecha fin para filtrar
        if fin is not None:
            fin = parse_date(fin)
            if not fin:
                return Response(
                    {"Mensaje": "Formato de fecha incorrecto. Usa YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Filtrar contratos a partir de la fecha fin indicada
            c3 = Contrato.objects.filter(fin__lte=fin)
        else:
            c3 = Contrato.objects.all()

        # Devuelve los contratos filtrados serializados al frontend
        contratos = c1 & c2 & c3
        contratos = contratos.order_by('-inicio')
        serializer = ContratoSerializer(contratos, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ConsultarEstadoBicicletaAPIView (APIView):
    """
    APIView para consultar el estado actual de una bicicleta del campus.
    Permite conocer si está en uso actualmente o en qué estación y anclaje se encuentra.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Obtención y validación datos de entrada
        id = request.data.get("id")

        if id is None:
            return Response(
                {"Mensaje": "Debe indicar la bicicleta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención de la bicicleta que se desea consultar a partir de su id
        bici = getBicicletaByID(id)
        if bici is None:
            return Response(
                {"Mensaje": "Bicicleta no encontrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtención del anclaje en el que se encuentra la bicicleta
        a = bici.anclajeBicicleta()
        if a is None:
            data = {"Mensaje": "Bicicleta en uso."}
        else:
            texto = str(a)
            texto = texto[0].lower() + texto[1:]
            data = {"Mensaje": f"Bicicleta ubicada en el {texto}."}

        return Response(
            data,
            status=status.HTTP_200_OK
        )


class TarifaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    APIView para obtener un listado de las tarifas existentes y que el usuario
    pueda seleccionar una mediante un desplegable en el frontend.
    """
    queryset = Tarifa.objects.all()
    serializer_class = TarifaListaSerializer
    permission_classes = []


class EstacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    APIView para obtener un listado de las estaciones existentes y que el usuario
    pueda seleccionar una mediante un desplegable en el frontend.
    """
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer
    permission_classes = []


class BicicletaAPIView(APIView):
    """
    APIView para obtener un listado de las bicicletas existentes y que el usuario
    pueda seleccionar una mediante un desplegable en el frontend.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "gestor":
            return Response(
                {"Mensaje": "Debes ser un gestor."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Devuelve las bicicletas del sistema serializadas al frontend
        serializer = BicicletaSerializer(Bicicleta.objects.all(), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetGestoresAPIView (APIView):
    """
    APIView para obtener un listado de los gestores existentes y que el usuario
    pueda seleccionar uno mediante un desplegable en el frontend.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verificar que el usuario que realiza la petición tiene el rol correcto
        user = request.user
        if user.getRol() != "administrador":
            return Response(
                {"Mensaje": "Debes ser un administrador."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Devuelve los gestores del sistema serializados al frontend
        serializer = GestorSerializer(Gestor.objects.all(), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
