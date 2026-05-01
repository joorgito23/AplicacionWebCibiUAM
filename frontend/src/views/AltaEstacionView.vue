<!-- src/views/AltaEstacionView.vue -->
<template>
  <div id="alta-estacion-view">
    <main>
      <h1 class="titulo-alta-estacion" data-cy="titulo-alta-est">
        Alta de Estación
      </h1>
      <div class="row justify-content-center mt-3">
        <div class="col-11 col-lg-8 d-flex justify-content-center">
          <p class="instrucciones">
            Esta sección permite dar de alta una nueva estación en el campus.
            Para ello, deberá introducir los campos solicitados en el formulario
            y, una vez validados, podrá dar de alta bicicletas para asignarlas a
            los anclajes de la nueva estación. Puede seleccionar un punto del
            mapa para obtener su ubicación y coordenadas.
          </p>
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Formulario alta de estación -->
        <div class="col-10 col-lg-4 d-flex justify-content-center">
          <div class="card card-cibiuam w-100">
            <h2 class="titulo text-center mb-3">
              <img src="/parking-de-bicicletas.png" alt="Parking" class="icono-titulo" />
              Detalles de la Estación
            </h2>
            <!-- Componente formulario de alta de estación -->
            <FormularioAltaEst @altaEstacion="crearEstacion" />
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
        <!-- Mapa del campus de la UAM -->
        <div class="col-12 col-lg-5">
          <MapaAltaEst />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import MapaAltaEst from "../components/MapaAltaEst.vue";
import FormularioAltaEst from "../components/FormularioAltaEst.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "alta-estacion-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const router = useRouter();

const mensajeError = ref("");
const mensaje = ref("");

// Función para crear una nueva estación a partir de los datos introducidos por el gestor
const crearEstacion = async (estacion) => {
  try {
    // Realiza una solicitud POST a la API para crear una estación nueva
    const response = await fetch(myVar + "/cibiuam/alta_estacion/", {
      method: "POST",
      body: JSON.stringify(estacion),
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
      }, 3000);
      return;
    }

    const data = await response.json();
    mensaje.value =
      data.Mensaje + " Serás redirigido automáticamente al menú inicial.";
    setTimeout(() => {
      router.push("/menu_gestor");
    }, 3000);
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.titulo-alta-estacion {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  padding: 0 1rem;
  margin-bottom: 0rem;
}

.btn-primary {
  margin: 10px;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
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
  text-align: center;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
}

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.5rem;
}
</style>
