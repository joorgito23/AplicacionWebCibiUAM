<!-- src/components/FiltrosReservasGestor.vue -->
<template>
  <div id="filtro-reserva-gestor">
    <div class="row mt-5 justify-content-center align-items-center">
      <!-- Estación de origen -->
      <div class="col-10 col-lg-4 mb-4 d-flex justify-content-lg-center text-center">
        <label for="origen" class="me-2">Estación Origen:</label>
        <select id="origen" v-model="filtros.origen" class="select-limitado" data-cy="select-reserva-origen">
          <option value="">-- Origen --</option>
          <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
            {{ estacion.nombre }}
          </option>
        </select>
      </div>
      <!-- Fecha de inicio -->
      <div class="col-10 col-lg-3 mb-4 d-flex justify-content-lg-center text-center">
        <label class="text-center" style="margin-right: 1rem">Fecha de inicio:</label>
        <input type="date" v-model="filtros.inicio" data-cy="inicio" />
      </div>
      <!-- Usuario -->
      <div class="col-10 col-lg-4 mb-4 d-flex justify-content-lg-center text-center">
        <label class="text-center" style="margin-right: 1rem">Usuario:</label>
        <input type="text" v-model="filtros.usuario" data-cy="usuario" placeholder="Escribe aquí..." />
      </div>
    </div>
    <div class="row justify-content-center align-items-center">
      <!-- Estación de destino -->
      <div class="col-10 col-lg-4 mb-4 d-flex justify-content-lg-center text-center">
        <label for="origen" class="me-2">Estación Destino:</label>
        <select id="destino" v-model="filtros.destino" class="select-limitado" data-cy="select-reserva-destino">
          <option value="">-- Destino --</option>
          <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
            {{ estacion.nombre }}
          </option>
        </select>
      </div>
      <!-- Fecha de fin -->
      <div class="col-10 col-lg-3 mb-4 d-flex justify-content-lg-center text-center">
        <label class="text-center" style="margin-right: 1rem">Fecha de fin:</label>
        <input type="date" v-model="filtros.fin" data-cy="fin" />
      </div>
      <!-- Botón filtrar reservas -->
      <div class="col-lg-4 col-10 d-flex justify-content-center">
        <button class="btn btn-primary" @click="filtrarReservas" data-cy="filtrar-boton">
          Filtrar Reservas
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "filtro-reserva-gestor" });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const mensajeError = ref("");

const filtros = ref({
  origen: "",
  destino: "",
  inicio: "",
  fin: "",
  usuario: "",
});

const emit = defineEmits(["filtrar-reservas-gestor"]);

// Función para enviar los filtros introducidos por el gestor a la vista correspondiente
const filtrarReservas = async () => {
  emit("filtrar-reservas-gestor", filtros.value);
};

const estaciones = ref([]);

// Función para obtener el listado de estaciones del sistema
const getEstaciones = async () => {
  try {
    // Realiza una solicitud GET para obtener las estaciones del campus
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = "Error al obtener informacion de las estaciones";
      return;
    }

    const data = await response.json();
    estaciones.value = data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getEstaciones();
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

.select-limitado {
  max-width: 50%;
  text-overflow: ellipsis;
}

input,
select {
  border-radius: 10px;
  border-color: rgb(0, 0, 0);
  background-color: white;
}
</style>
