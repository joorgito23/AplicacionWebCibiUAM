<!-- src/components/FormularioAltaEst.vue -->
<template>
  <div id="formulario-alta-estacion" style="width: 100%">
    <form @submit.prevent="altaEstacion">
      <div style="width: 100%">
        <div class="row justify-content-center">
          <!-- Nombre de la estación -->
          <div class="col-md-12 col-12 d-flex flex-column justify-content-center mb-3">
            <label class="align-self-start"><span class="text-danger">*</span> Nombre:</label>
            <input v-model="estacion.nombre" type="text" class="form-control" placeholder="Escriba aquí..."
              data-cy="est-nombre" />
          </div>
        </div>
        <div class="row justify-content-center">
          <!-- Ubicación -->
          <div class="col-md-12 col-12 d-flex flex-column justify-content-center mb-3">
            <label class="align-self-start"><span class="text-danger">*</span> Ubicación:</label>
            <input v-model="estacion.ubicacion" type="text" class="form-control" placeholder="Escriba aquí..."
              data-cy="est-ubicacion" />
          </div>
        </div>
        <div class="row align-items-center justify-content-center">
          <!-- Número de anclajes -->
          <div class="col-md-12 col-12 d-flex flex-column justify-content-center mb-3">
            <label class="align-self-start"><span class="text-danger">*</span> Número de Anclajes:</label>
            <input v-model="estacion.nAnclajes" type="number" step="1" min="1" class="form-control"
              placeholder="Introduzca número" data-cy="est-anc" />
          </div>
        </div>
        <div class="row align-items-center justify-content-center">
          <!-- Latitud -->
          <div class="col-md-12 col-12 d-flex flex-column justify-content-center mb-3">
            <label class="align-self-start"><span class="text-danger">*</span> Latitud:</label>
            <input v-model="estacion.latitud" type="text" class="form-control"
              placeholder="Coordenadas con punto decimal" data-cy="est-lat" />
          </div>
        </div>
        <div class="row align-items-center justify-content-center">
          <!-- Longitud -->
          <div class="col-md-12 col-12 d-flex flex-column justify-content-center mb-3">
            <label class="align-self-start"><span class="text-danger">*</span> Longitud:</label>
            <input v-model="estacion.longitud" type="text" class="form-control"
              placeholder="Coordenadas con punto decimal" data-cy="est-long" />
          </div>
        </div>
        <div class="row justify-content-center">
          <!-- Botón alta de estación -->
          <div class="col-auto">
            <div class="form-group">
              <button class="btn btn-primary" data-cy="alta-est-boton">
                Alta Estación
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";

defineOptions({
  name: "formulario-alta-estacion",
});

const estacion = ref({
  nombre: "",
  ubicacion: "",
  nAnclajes: "",
  latitud: "",
  longitud: "",
});

const emit = defineEmits(["altaEstacion"]);

// Función que envía los detalles de la nueva estación a la vista correspondiente
const altaEstacion = () => {
  emit("altaEstacion", estacion.value);
};
</script>

<style scoped>
.btn-primary {
  margin: 10px;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
  margin-bottom: 1rem;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}
</style>
