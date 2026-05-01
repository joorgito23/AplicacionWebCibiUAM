<!-- src/views/ConsultarEstadoView.vue -->
<template>
  <div id="estado-view">
    <main>
      <h1 class="titulo-estado" data-cy="titulo-estado">
        Estado del Campus de la UAM
      </h1>
      <div class="row justify-content-center mt-3">
        <div class="col-12 col-lg-8 d-flex justify-content-center mb-2">
          <p class="instrucciones">
            Esta sección permite conocer el estado actual del campus de la UAM.
            Para cada estación disponible del campus, podrá conocer el número de
            bicicletas que hay disponibles, así como el número de anclajes
            libres para devolver una bicicleta y la ubicación en la que se
            encuentra la estación seleccionada.
          </p>
        </div>
      </div>
      <div class="row justify-content-center align-items-center">
        <!-- Información de cada estación del campus-->
        <div class="col-12 col-lg-6">
          <EstadoCampus @marcar="marcarEstacion" :estacionEstado="estacionEstado" />
        </div>
        <!-- Mapa del campus -->
        <div class="col-12 col-lg-5">
          <MapaCampus :estacionMarcada="estacion" @mostrarEstado="mostrarEstado" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import EstadoCampus from "../components/EstadoCampus.vue";
import MapaCampus from "../components/MapaCampus.vue";
import { ref } from "vue";
defineOptions({ name: "estado-view" });

const estacion = ref(null);

// Función para enviar al mapa la estación que debe resaltar
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

.instrucciones {
  text-align: justify;
  margin: 0 auto 2rem auto;
  padding: 0 2rem;
}
</style>
