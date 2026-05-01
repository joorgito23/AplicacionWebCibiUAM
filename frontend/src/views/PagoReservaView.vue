<!-- src/views/PagoReservaView.vue-->
<template>
  <div id="pago-reserva-view" class="pago-reserva-container">
    <main>
      <h1 class="titulo-pago-reserva">Pago de la Reserva</h1>
      <div class="row justify-content-center mt-3">
        <!-- Detalles de la reserva -->
        <div class="col-11 col-lg-5 col-md-10 d-flex justify-content-center mb-2">
          <div class="card card-cibiuam w-100">
            <h2 class="titulo">
              <img src="/informacion.png" alt="Info" class="icono-titulo" />
              Información general de la reserva
            </h2>
            <div class="info">
              <span><strong><img src="/entrega.png" alt="Fecha" class="icono" />
                  Inicio: </strong>
                <span class="detalles">{{ inicio }}</span></span>
              <span><strong><img src="/entrega.png" alt="Fecha" class="icono" />
                  Fin: </strong>
                <span class="detalles">{{ fin }}</span></span>
              <span><strong><img src="/reloj.png" alt="Hora" class="icono" /> Hora de
                  Inicio: </strong>
                <span class="detalles">{{ horaInicio }}</span></span>
              <span><strong><img src="/reloj.png" alt="Hora" class="icono" /> Hora de
                  Fin: </strong>
                <span class="detalles">{{ horaFin }}</span></span>
              <span><strong><img src="/parking-de-bicicletas.png" alt="Estacion" class="icono" />
                  Origen: </strong>
                <span class="detalles">{{ origen }}</span></span>
              <span><strong><img src="/parking-de-bicicletas.png" alt="Estacion" class="icono" />
                  Destino: </strong>
                <span class="detalles">{{ destino }}</span></span>
            </div>
          </div>
        </div>
        <!-- Factura de la reserva -->
        <div class="col-11 col-lg-5 col-md-10 d-flex justify-content-center mb-2">
          <div class="card card-cibiuam w-100">
            <h2 class="titulo">🧾 Recibo de la reserva</h2>
            <div class="info">
              <span><strong><img src="/billete-de-banco.png" alt="Euro" class="icono" />
                  Importe: </strong>
                <span class="detalles">{{ importe }}€</span></span>
              <span><strong><img src="/entrega.png" alt="Fecha" class="icono" />
                  Cancelable hasta: </strong>
                <span class="detalles">{{ cancelacion }}</span></span>
            </div>
            <!-- Renderizado botón de pago paypal -->
            <div class="contenedor-pago">
              <div ref="paypal" class="paypal"></div>
            </div>
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success" data-cy="msg">{{ mensaje }}</p>
              </div>
              <div v-if="mensajeError">
                <p class="alert alert-danger">{{ mensajeError }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { useDatosPagoReserva } from "@/stores/datosPagoReserva";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "pago-reserva-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const router = useRouter();
const pagoStore = useDatosPagoReserva();
const authStore = useAuthStore();
const importe = pagoStore.importe;
const order_id = pagoStore.order_id;
const reserva_id = pagoStore.reserva_id;
const saldo = pagoStore.saldo;
const inicio = pagoStore.inicio;
const fin = pagoStore.fin;
const horaInicio = pagoStore.horaInicio;
const horaFin = pagoStore.horaFin;
const origen = pagoStore.origen;
const destino = pagoStore.destino;
const mensaje = ref("");
const mensajeError = ref("");
const paypal = ref(null);

onMounted(() => {
  if (paypal.value) {
    // Renderiza el botón de pago
    window.paypal
      .Buttons({
        // Función para crear la orden de pago
        createOrder() {
          return order_id;
        },

        // Función para aprobar el pago
        onApprove: async () => {
          const datos = {
            order_id: order_id,
            reserva_id: reserva_id,
            saldo: saldo,
          };
          // Realiza post a la API para realizar el pago
          const response = await fetch(myVar + "/cibiuam/pagar_reserva/", {
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
              "Ocurrió un error inesperado al validar el pago. Vuelva a realizar la reserva.";

            setTimeout(() => {
              mensajeError.value = "";
            }, 3000);
          } else {
            const data = await response.json();
            mensaje.value =
              data.Mensaje +
              "\n Serás redirigido a la pantalla de inicio automáticamente.";
          }

          // Limpia datos del pago almacenados previamente
          pagoStore.clearPago();
          setTimeout(() => {
            router.push("/menu_usuario");
          }, 4000);
        },

        // Función para cancelar el pago
        onCancel: () => {
          mensajeError.value = "Pago cancelado por el usuario";
          setTimeout(() => {
            mensajeError.value = "";
          }, 3000);
        },

        // Función de error durante el pago
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

// Función para obtener la fecha límite de cancelación de la reserva
const horaLimiteCancelacion = (fecha, hora) => {
  const fechaInicioReserva = new Date(`${fecha}T${hora}`);
  fechaInicioReserva.setHours(fechaInicioReserva.getHours() - 1);

  // Añade un 0 si tiene 1 sola cifra
  const padding = (n) => String(n).padStart(2, "0");

  const yyyy = fechaInicioReserva.getFullYear();
  const mm = padding(fechaInicioReserva.getMonth() + 1);
  const dd = padding(fechaInicioReserva.getDate());
  const hh = padding(fechaInicioReserva.getHours());
  const min = padding(fechaInicioReserva.getMinutes());
  const ss = padding(fechaInicioReserva.getSeconds());

  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
};

const cancelacion = horaLimiteCancelacion(inicio, horaInicio);
</script>
<style scoped>
.pago-reserva-container {
  width: 100%;
}

.titulo-pago-reserva {
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
  color: black;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
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
  padding: 10px 2px;
  line-height: 1.8;
}

.detalles {
  color: black;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 1rem;
}

.contenedor-pago {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  width: 100%;
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
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-right: 0.25rem;
}
</style>
