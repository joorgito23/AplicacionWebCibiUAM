<!-- src/componets/SelectorTarifaAlta.vue -->
<template>
  <div id="selector-tarifa-alta" class="d-flex flex-column">
    <label for="tarifa" :class="labelClass"><span class="text-danger">*</span> Seleccione una tarifa:</label>
    <select id="tarifa" v-model="tarifaSeleccionada" @change="enviarTarifa" data-cy="select-tarifa-alta"
      class="form-select">
      <option value="">-- Seleccione --</option>
      <option v-for="tarifa in tarifas" :key="tarifa.duracion" :value="tarifa.duracion">
        {{ tarifa.duracion }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineOptions({ name: "selector-tarifa-alta" });
defineProps({ labelClass: { type: String, default: "" } });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const tarifas = ref([]);
const tarifaSeleccionada = ref("");

// Función para obtener las tarifas disponibles
const getTarifas = async () => {
  try {
    // Realiza una solicitud GET para obtener las tarifas existentes
    const response = await fetch(myVar + "/cibiuam/informacion/tarifas/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    const data = await response.json();
    tarifas.value = data;
  } catch (error) {
    console.error(error);
  }
};

const emit = defineEmits(["enviar-tarifa"]);

// Función que envía la tarifa seleccionada por el usuario a la vista correspondiente
const enviarTarifa = async () => {
  if (!tarifaSeleccionada.value) {
    return;
  }

  emit("enviar-tarifa", tarifaSeleccionada.value);
};

onMounted(() => {
  getTarifas();
});
</script>

<style scoped>
.form-select {
  border-radius: 5px;
  padding: 0.5rem 1rem;
}
</style>
