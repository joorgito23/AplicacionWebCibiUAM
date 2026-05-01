<!-- src/views/PagoAltaUsuarioView.vue-->
<template>
  <div id="pago-alta-view">
    <main>
      <div class="contenedor-main">
        <h1 class="pago-alta-title">Pago Alta de Usuario</h1>
        <p class="instrucciones">
          A continuación se adjunta la factura correspondiente para crear la
          cuenta de usuario. En caso de estar conforme proceda al pago o, en
          caso contrario, vuelva al menú inicial y cancele el proceso de alta.
        </p>
        <!-- Información de la factura -->
        <div class="card col-auto d-flex flex-column justify-content-center">
          <h2 class="titulo-tarjeta">
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
        <!-- Renderizado botón de pago paypal -->
        <div class="contenedor-pago">
          <div ref="paypal" class="paypal"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

defineOptions({ name: "pago-alta-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
import { ref, onMounted } from "vue";
const router = useRouter();
import { useDatosPago } from "@/stores/datosPago";
const pagoStore = useDatosPago();
const usuario = pagoStore.usuario;
const importe = pagoStore.importe;
const fin = pagoStore.fin;
const order_id = pagoStore.order_id;
const user_id = pagoStore.user_id;
const mensaje = ref("");
const mensajeError = ref("");
const paypal = ref(null);

// Ejecución después de que Vue haya renderizado el componente en el DOM
onMounted(() => {
  if (paypal.value) {
    // Renderizamos el botón de PayPal
    window.paypal
      .Buttons({
        // Función crear orden de pago
        createOrder() {
          return order_id;
        },

        // Aprobación del pago
        onApprove: async () => {
          // Petición a la API para realizar el pago
          const datos = { order_id: order_id, user_id: user_id };
          const response = await fetch(myVar + "/cibiuam/pagar/", {
            method: "POST",
            body: JSON.stringify(datos),
            headers: { "Content-type": "application/json; charset=UTF-8" },
          });
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Error:", errorData);
            mensajeError.value =
              "Ocurrió un error inesperado al validar el pago. Vuelva a crear el usuario.";
            setTimeout(() => {
              mensajeError.value = "";
            }, 3000);
          } else {
            const data = await response.json();
            mensaje.value =
              data.Mensaje +
              "\n Serás redirigido a la pantalla de inicio automáticamente.";
          }

          // Limpiamos datos de pago guardados previamente
          pagoStore.clearPago();
          setTimeout(() => {
            router.push("/");
          }, 5000);
        },
        // Función cancelación de pago
        onCancel: () => {
          mensajeError.value = "Pago cancelado por el usuario";
          setTimeout(() => {
            mensajeError.value = "";
          }, 5000);
        },

        // Función error de pago
        onError: () => {
          mensajeError.value = "Error de PayPal. Inténtalo de nuevo";
          setTimeout(() => {
            mensajeError.value = "";
          }, 5000);
        },
      })
      .render(paypal.value);
  }
});
</script>

<style scoped>
.contenedor-main {
  max-width: 768px;
  margin: 0 auto;
}

.pago-alta-title {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin-right: 1rem;
  margin-left: 1rem;
  margin-bottom: 0.25rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  width: 90%;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 30px auto;
}

.titulo-tarjeta {
  margin-bottom: 16px;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 16px;
}

@media (min-width: 768px) {
  .info {
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 18px;
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

.contenedor-pago {
  display: flex;
  justify-content: center;
  width: 100%;
}

.paypal {
  width: 90%;
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
