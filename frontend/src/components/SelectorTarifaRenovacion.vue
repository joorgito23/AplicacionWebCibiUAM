<!-- src/components/SelectorTarifaRenovacion.vue -->
<template>
  <div id="selector-tarifa-reno">
    <!-- Selector de tarifa -->
    <div class="row mb-3 justify-content-center align-items-center">
      <div class="col-12 col-lg-10 mb-2 d-flex justify-content-center text-center">
        <label class="me-2" for="tarifa">Seleccione tarifa de renovación:</label>
        <select id="tarifa" v-model="tarifaSeleccionada" data-cy="select-tarifa" class="select-reno">
          <option value="">-- Seleccione --</option>
          <option v-for="tarifa in tarifas" :key="tarifa.duracion" :value="tarifa.duracion">
            {{ tarifa.duracion }}
          </option>
        </select>
      </div>
    </div>
    <!-- Botón de renovación -->
    <div class="row justify-content-center">
      <div class="col-auto">
        <button class="btn btn-primary" @click="tarifaRenovacion" data-cy="renovar-boton">
          Renovar Contrato
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "selector-tarifa-reno" });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const tarifas = ref([]);
const tarifaSeleccionada = ref("");
const mensajeError = ref("");

// Función que obtiene las tarifas disponibles en la aplicación
const getTarifas = async () => {
  try {
    // Realiza una solicitud GET para obtener las tarifas
    const response = await fetch(myVar + "/cibiuam/informacion/tarifas/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = "Error al obtener informacion de las tarifas";
      return;
    }

    const data = await response.json();
    tarifas.value = data;
  } catch (error) {
    console.error(error);
  }
};

const emit = defineEmits(["tarifa-renovacion"]);
// Envía la tarifa seleccionada por el usuario a la vista de renovación
const tarifaRenovacion = async () => {
  if (!tarifaSeleccionada.value) {
    alert("Por favor selecciona una tarifa");
    return;
  }

  emit("tarifa-renovacion", tarifaSeleccionada.value);
};

onMounted(() => {
  getTarifas();
});
</script>

<style scoped>
.btn-primary {
  margin-top: 0.5rem;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}

.select-reno {
  border-radius: 10px;
  text-overflow: ellipsis;
}
</style>
