import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from rest_framework import status
from pagosPayPal.models import Pagos


class PayPal:
    @staticmethod
    def obtener_paypal_token():
        """
        Método que permite obtener el token de acceso a PayPal
        para realizar la creación y captura de la orden de pago
        a partir de CLIENT_ID y SECRET_ID.
        """
        # Construcción cabecera y datos de la petición
        url = f"{settings.PAYPAL_BASE}/v1/oauth2/token"
        headers = {
            "Accept": "application/json"
        }
        data = {"grant_type": "client_credentials"}

        # Petición a la API de PayPal
        response = requests.post(
            url,
            headers=headers,
            data=data,
            auth=HTTPBasicAuth(
                settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET
            )
        )

        # Devolución del token de acceso
        if response.status_code == 200:
            return response.json()["access_token"]

        return None

    @staticmethod
    def crear_orden(importe):
        """
        Método para crear la orden de pago indicando importe.
        """

        # Validación datos
        if importe <= 0:
            return Response({"Mensaje": "Importe inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtención del token de acceso
        token = PayPal.obtener_paypal_token()

        if token is None:
            return Response({"Mensaje": "No se pudo generar el token"}, status=status.HTTP_400_BAD_REQUEST)

        # Creación request
        url = f"{settings.PAYPAL_BASE}/v2/checkout/orders"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        body = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "EUR",
                    "value": importe
                }
            }]
        }

        # Realización de POST a la API de PayPal para crear la orden y obtener order id
        response = requests.post(url, json=body, headers=headers)
        if response.status_code != status.HTTP_201_CREATED:
            return Response({"Mensaje": "Error al tratar de crear el pago"}, status=status.HTTP_400_BAD_REQUEST)

        # Registro order_id en el sistema
        Pagos.objects.create(order_id=str(
            response.json().get("id")), pagado=False)
        return Response({"order_id": response.json().get("id"), "importe": importe}, status=status.HTTP_201_CREATED)

    @staticmethod
    def capturar_orden(order_id):
        """
        Método que realiza la captura de la orden y permite la
        transacción del importe de pago de una cuenta a otra una vez el pago
        ha sido aprobado por el usuario.
        """

        # Obtención del token
        token = PayPal.obtener_paypal_token()

        if token is None:
            return Response({"Mensaje": "No se pudo generar el token"}, status=status.HTTP_400_BAD_REQUEST)

        url = f"{settings.PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Post a la API de PayPal para capturar la orden de pago y obtener el estado del pago
        response = requests.post(url, headers=headers)
        if response.status_code != status.HTTP_200_OK and response.status_code != status.HTTP_201_CREATED:
            return Response({"Error": "Ocurrió un error al procesar el pago"}, status=status.HTTP_400_BAD_REQUEST)

        # Comprobación estado del pago
        data = response.json()
        if data['status'] != 'COMPLETED':
            return Response({"Error": "Pago no realizado"}, status=status.HTTP_400_BAD_REQUEST)

        # Comprobación order_id no ha sigo pagado previamente
        estado = Pagos.objects.filter(order_id=str(order_id)).first()
        if estado is None:
            return Response({"Error": "Pago no encontrado en la base de datos"}, status=status.HTTP_400_BAD_REQUEST)

        if estado.pagado:
            return Response({"Error": "Pago ya realizado"}, status=status.HTTP_400_BAD_REQUEST)

        estado.pagado = True
        estado.save()

        return Response({"Mensaje": "Pago realizado con éxito"}, status=response.status_code)
