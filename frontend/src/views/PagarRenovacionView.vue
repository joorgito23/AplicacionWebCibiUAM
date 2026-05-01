<!-- src/views/PagarRenovaciónView.vue -->
<template>
  <div id="pago-renovacion-view" style="width: 100%">
    <main>
      <h1 class="titulo-pago-renovacion">Pago de la Renovación del Contrato</h1>
      <!-- Información de la factura de renovación -->
      <div class="row justify-content-center mt-2">
        <div class="col-lg-4 col-md-8 col-11 d-flex flex-column justify-content-center">
          <div class="card card-cibiuam w-100">
            <h2 class="titulo">
            <img src="/informacion.png" alt="Info" class="icono-titulo" />
            Información general de la factura
          </h2>
            <div class="info">
              <span><strong><img src="/user.png" alt="User" class="icono" />
                  Usuario: </strong>
                <span class="detalle">{{ usuario }}</span></span>
              <span><strong><img src="/euro.png" alt="Euro" class="icono" />
                  Importe: </strong>
                <span class="detalle">{{ importe }}€</span></span>
              <span><strong><img src="/contrato.png" alt="Fin" class="icono" />
                  Finalización del contrato: </strong>
                <span class="detalle">{{ fin }}</span></span>
            </div>
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success">{{ mensaje }}</p>
              </div>
              <div v-if="mensajeError">
                <p class="alert alert-danger">{{ mensajeError }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Renderizado del botón de pago de paypal -->
      <div class="row justify-content-center mt-1">
        <div class="col-lg-4 col-md-8 col-11">
          <div ref="paypal" class="paypal"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { useDatosPagoRenovacion } from "@/stores/datosPagoRenovacion";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "pago-renovacion-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
const router = useRouter();
const pagoStore = useDatosPagoRenovacion();
const authStore = useAuthStore();

const usuario = pagoStore.usuario;
const importe = pagoStore.importe;
const fin = pagoStore.fin;
const order_id = pagoStore.order_id;
const user_id = pagoStore.user_id;
const tarifa = pagoStore.tarifa;
const mensaje = ref("");
const mensajeError = ref("");
const paypal = ref(null);

onMounted(() => {
  if (paypal.value) {
    // Renderiza el botón de pago de PayPal
    window.paypal
      .Buttons({
        // Función para crear orden de pago
        createOrder() {
          return order_id;
        },

        // Función de aprobación de pago
        onApprove: async () => {
          const datos = {
            order_id: order_id,
            user_id: user_id,
            tarifa: tarifa,
          };

          // Petición POST a la API para realizar el pago
          const response = await fetch(myVar + "/cibiuam/pagar_renovacion/", {
            method: "POST",
            body: JSON.stringify(datos),
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + authStore.token,
            },
          });
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Error:", errorData);
            mensajeError.value =
              "Ocurrió un error inesperado al validar el pago. Vuelva a renovar el contrato.";
            setTimeout(() => {
              mensajeError.value = "";
            }, 3000);
          } else {
            const data = await response.json();
            mensaje.value =
              data.Mensaje +
              "\n Serás redirigido a la pantalla de inicio automáticamente.";
          }

          // Limpiamos datos almacenados previamente para el pago
          pagoStore.clearPago();
          setTimeout(() => {
            router.push("/menu_usuario");
          }, 5000);
        },

        // Función de cancelación del pago por el usuario
        onCancel: () => {
          mensajeError.value = "Pago cancelado por el usuario";
          setTimeout(() => {
            mensajeError.value = "";
          }, 3000);
        },

        // Función de error en el pago
        onError: () => {
          mensajeError.value = "Error de PayPal. Inténtalo de nuevo";
          setTimeout(() => {
            mensajeError.value = "";
          }, 3000);
        },
      })
      .render(paypal.value);
  }
});
</script>
<style scoped>
.titulo-pago-renovacion {
  text-align: center;
  margin-top: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 20px auto;
}

.titulo {
  margin-bottom: 16px;
  font-family: "DM Sans", sans-serif;
  font-weight: 300;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 16px;
  color: rgb(52, 52, 52);
}

@media (min-width: 768px) {
  .info {
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 18px;
    color: rgb(52, 52, 52);
  }
}

.info span {
  background: #eff6ff;
  border-radius: 6px;
  padding: 10px 1px;
  line-height: 1.8;
}

.detalle {
  color: black;
  font-weight: 600;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 1rem;
}

.paypal {
  width: 100%;
}

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.25rem;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
  margin-right: 0.25rem;
}
</style>
