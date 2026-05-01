from django.urls import path, include

from sgu_sgs.views.sgu_views import *
from sgu_sgs.views.sgs_views import *
from rest_framework import routers
router = routers.DefaultRouter()

router.register('tarifas', TarifaViewSet)
router.register('estaciones', EstacionViewSet)
urlpatterns = [
    path(r'alta_gestor/', AltaGestorAPIView.as_view()),
    path(r'baja_gestor/', BajaGestorAPIView.as_view()),
    path(r'actualizar_tarifa/', ActualizarTarifaAPIView.as_view()),
    path(r'consultar_tarifa/', ConsultarTarifaAPIView.as_view()),
    path(r'alta_estacion/', AltaEstacionAPIView.as_view()),
    path(r'alta_bicicleta/', AltaBicicletaAPIView.as_view()),
    path(r'crear_usuario/', CrearCuentaUsuarioAPIView.as_view()),
    path(r'pagar/', PagarAltaUsuarioAPIView.as_view()),
    path(r'consultar_perfil/', ConsultarPerfilAPIView.as_view()),
    path(r'modificar_perfil/', ModificarPerfilAPIView.as_view()),
    path(r'renovar_contrato/', RenovarContratoAPIView.as_view()),
    path(r'pagar_renovacion/', PagarRenovacionContratoAPIView.as_view()),
    path(r'leer_notificaciones/', LeerNotificacionesAPIView.as_view()),
    path(r'consultar_estado/', ConsultarEstadoCampusAPIView.as_view()),
    path(r'consultar_contratos/', ConsultarContratosAPIView.as_view()),
    path(r'consultar_contratos_filtros/',
         ConsultarContratosFiltrosAPIView.as_view()),
    path(r'consultar_estado_bicicleta/',
         ConsultarEstadoBicicletaAPIView.as_view()),
    path(r'informacion/', include(router.urls)),
    path(r'informacion/gestores/', GetGestoresAPIView.as_view()),
    path(r'informacion/bicicletas/', BicicletaAPIView.as_view()),
]
