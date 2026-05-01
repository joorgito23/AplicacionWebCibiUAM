from django.urls import path
from sgr.views.sgr_views import HacerReservaAPIView, PagarReservaAPIView, CancelarReservaAPIView, ConsultarReservasAPIView, ConsultarReservasFiltrosAPIView

urlpatterns = [
    path(r'hacer_reserva/', HacerReservaAPIView.as_view()),
    path(r'pagar_reserva/', PagarReservaAPIView.as_view()),
    path(r'cancelar_reserva/', CancelarReservaAPIView.as_view()),
    path(r'consultar_reservas/', ConsultarReservasAPIView.as_view()),
    path(r'consultar_reservas_filtros/',
         ConsultarReservasFiltrosAPIView.as_view()),

]
