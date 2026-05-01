<!-- src/views/RealizarReservaView.vue -->
<template>
  <div id="reserva-view" class="reserva-container">
    <main>
      <h1 class="titulo-reservas" data-cy="reserva-tit">Realizar Reserva</h1>
      <div class="row justify-content-center mt-3">
        <div class="col-10 col-lg-6 d-flex justify-content-center mb-2">
          <p class="instrucciones">
            En esta pantalla podrás reservar una bicicleta indicando los campos
            solicitados a continuación. Recuerde que no puede realizar más de
            una reserva en la misma franja horaria.
          </p>
        </div>
      </div>
      <div class="row justify-content-center mt-3">
        <!-- Formulario de reserva -->
        <div class="col-11 col-lg-5 justify-content-center">
          <div class="card card-cibiuam">
            <h2 class="titulo">Detalles de la Reserva</h2>
            <!-- Componente formulario de reserva -->
            <FormularioReserva @reserva="crearReserva" />
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
        <!-- Mapa del campus -->
        <div class="col-12 col-lg-6">
          <MapaCampusReserva />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FormularioReserva from "../components/FormularioReserva.vue";
import MapaCampusReserva from "../components/MapaCampusReserva.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useDatosPagoReserva } from "@/stores/datosPagoReserva";
defineOptions({ name: "reserva-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const pagoStore = useDatosPagoReserva();
const router = useRouter();

const mensajeError = ref("");
const mensaje = ref("");

// Función que realiza una nueva reserva a partir del formulario disponible
const crearReserva = async (reserva) => {
  try {
    // Realiza una solicitud POST a la API para realizar una reserva
    const response = await fetch(myVar + "/cibiuam/hacer_reserva/", {
      method: "POST",
      body: JSON.stringify(reserva),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeError.value = "";
      }, 4000);
      return;
    }

    const data = await response.json();

    // Si no tiene coste, redirige al usuario al menú inicial. En caso contrario, envía al usuario a la pantalla de pago
    if (Math.abs(Number(data.importe)) < 0.000001) {
      mensaje.value =
        data.Mensaje + " Serás redirigido automáticamente al menú inicial.";
      setTimeout(() => {
        mensaje.value = "";
      }, 4000);
      setTimeout(() => {
        router.push("/menu_usuario");
      }, 4000);
    } else {
      // Guarda datos necesarios para proceder al pago en la siguiente pantalla y redirige a la pantalla de pago
      pagoStore.setPago(
        data.order_id,
        data.reserva_id,
        data.saldo,
        data.importe,
        data.inicio,
        data.fin,
        data.horaInicio,
        data.horaFin,
        data.origen,
        data.destino
      );
      router.push("/pagar_reserva");
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.reserva-container {
  width: 100%;
}

.titulo-reservas {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin: 0 auto 1rem auto;
  padding: 0 1rem;
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

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
}

.titulo {
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}
</style>
