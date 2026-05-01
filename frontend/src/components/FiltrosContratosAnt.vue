<!-- src/components/FiltrosContratos.vue -->
<template>
  <div id="filtros-contratos">
    <div class="row mb-4 justify-content-center align-items-center">
      <div class="col-12 d-flex justify-content-center">
        <label for="tarifa" class="text-center" style="margin-right: 1rem">Seleccione una tarifa:</label>
        <select id="tarifa" v-model="filtros.tarifa" data-cy="select-tarifa"
          style="border-radius: 10px; background-color: white">
          <option value="">-- Seleccione --</option>
          <option v-for="tarifa in tarifas" :key="tarifa.duracion" :value="tarifa.duracion">
            {{ tarifa.duracion }}
          </option>
        </select>
      </div>
    </div>
    <div class="row mb-4 justify-content-center align-items-center">
      <div class="col-12 d-flex justify-content-center">
        <label class="text-center" style="margin-right: 1rem">Fecha de inicio:</label>
        <input type="date" v-model="filtros.inicio" data-cy="inicio"
          style="border-radius: 10px; background-color: white" />
      </div>
    </div>
    <div class="row mb-3 justify-content-center align-items-center">
      <div class="col-12 d-flex justify-content-center">
        <label class="text-center" style="margin-right: 1rem">Fecha de fin:</label>
        <input type="date" v-model="filtros.fin" data-cy="fin" style="border-radius: 10px; background-color: white" />
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-auto">
        <button class="btn btn-primary" @click="filtrarContratos" data-cy="filtrar-boton">
          Filtrar Contratos
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "filtros-contratos" });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const tarifas = ref([]);
const mensajeError = ref("");

// Función que obtiene las tarifas disponibles en la aplicación
const getTarifas = async () => {
  try {
    // Realiza una solicitud GET para obtener las tarifas de CibiUAM
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

const filtros = ref({
  tarifa: "",
  inicio: "",
  fin: "",
});
const emit = defineEmits(["filtrar-contratos"]);

// Función que envía los filtros establecidos por el gestor a la vista correspondiente
const filtrarContratos = async () => {
  emit("filtrar-contratos", filtros.value);
};

onMounted(() => {
  getTarifas();
});
</script>

<style scoped>
.btn-primary {
  margin: 10px;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}

.input {
  border-radius: 10px;
}
</style>
