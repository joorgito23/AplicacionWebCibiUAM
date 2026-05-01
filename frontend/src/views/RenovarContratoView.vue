<!-- src/views/RenovarContratoView.vue -->
<template>
  <div id="renovar-contrato">
    <main>
      <div class="row justify-content-center">
        <div class="col-11 col-lg-7 d-flex justify-content-center">
          <div class="card card-cibiuam">
            <h1 class="titulo-renovar">Renovación del Contrato</h1>
            <p class="instrucciones">
              Esta sección permite renovar el contrato de uso del usuario. Para
              ello, deberá seleccionar la tarifa que desee para su nuevo
              contrato y será redirigido automáticamente a la pantalla de pago
              para finalizar la renovación. Una vez renovado el contrato y
              cuando finalice el contrato actual, podrá disfrutar de la nueva
              tarifa seleccionada.
            </p>
            <!-- Selector de tarifa de renovación -->
            <SelectorTarifaRenovacion @tarifa-renovacion="renovar" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import SelectorTarifaRenovacion from "../components/SelectorTarifaRenovacion.vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useDatosPagoRenovacion } from "@/stores/datosPagoRenovacion";
defineOptions({ name: "renovar-contrato" });

const myVar = import.meta.env.VITE_DJANGOURL;
const router = useRouter();
const authStore = useAuthStore();
const pagoStore = useDatosPagoRenovacion();

// Función que realiza la renovación del contrato de un usuario
const renovar = async (tarifaSeleccionada) => {
  try {
    // Realiza una solicitud POST para renovar el contrato
    const response = await fetch(myVar + "/cibiuam/renovar_contrato/", {
      method: "POST",
      body: JSON.stringify({ tarifa: tarifaSeleccionada }),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    const data = await response.json();

    // Guarda datos necesarios para proceder al pago de la renovación
    pagoStore.setPago(
      data.order_id,
      data.user_id,
      authStore.usuario,
      data.importe,
      data.fin,
      tarifaSeleccionada
    );
    // Redirige a la pantalla de pago
    router.push("/pagar_renovacion");
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 30px 20px;
}

.titulo-renovar {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin: 1rem auto 2rem auto;
}
</style>
