<!-- src/views/ConsultarEstadoGestorView.vue -->
<template>
  <div id="estado-view" style="width: 100%">
    <main>
      <h1 class="titulo-estado">Estado de Bicicletas y Estaciones</h1>
      <div class="row justify-content-center">
        <div class="col-12 col-lg-6">
          <!-- Estado de estaciones -->
          <EstadoCampus @marcar="marcarEstacion" :estacionEstado="estacionEstado" v-if="vista === 'estaciones'" />
          <!-- Estado de bicicletas -->
          <EstadoGestor v-else />
          <!-- Botón para que el gestor seleccione si desea consultar el estado de las estaciones o bicicletas -->
          <div class="d-flex justify-content-center gap-2 mb-3">
            <button v-if="vista === 'bicis'" class="btn btn-primary" @click="vista = 'estaciones'">
              Consultar Estado de Estaciones
            </button>
            <button v-else class="btn btn-primary" @click="vista = 'bicis'" data-cy="estado-bicis">
              Consultar Estado de Bicicletas
            </button>
          </div>
        </div>
        <div class="col-12 col-lg-5">
          <!-- Mapa del campus -->
          <MapaCampus :estacionMarcada="estacion" @mostrarEstado="mostrarEstado" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import EstadoCampus from "../components/EstadoCampus.vue";
import EstadoGestor from "../components/EstadoGestor.vue";
import MapaCampus from "../components/MapaCampus.vue";
import { ref } from "vue";
defineOptions({ name: "estado-view" });

const vista = ref("estaciones");
const estacion = ref(null);

// Función para enviar la estación consultada por el usuario al mapa y mostrar su ubicación
const marcarEstacion = async (est) => {
  estacion.value = est;
  return;
};

const estacionEstado = ref(null);

// Función para enviar desde el mapa la estación de la que debe mostrar el estado
const mostrarEstado = async (est) => {
  estacionEstado.value = est;
  return;
};
</script>

<style scoped>
.titulo-estado {
  text-align: center;
  margin: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
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
</style>
