<!-- src/componets/FormularioReserva.vue -->
<template>
  <div id="formulario-reserva">
    <form @submit.prevent="hacerReserva">
      <div class="row justify-content-center align-items-center">
        <!-- Estación de origen -->
        <div class="col-12 col-md-6 mb-3 d-flex flex-column text-center text-md-start">
          <label class="align-self-start" for="origen">Seleccione Origen:</label>
          <select id="origen" v-model="reserva.origen" class="select-limitado" data-cy="select-reserva-origen">
            <option value="">-- Origen --</option>
            <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
              {{ estacion.nombre }}
            </option>
          </select>
        </div>
        <!-- Estación de destino -->
        <div class="col-12 col-md-6 mb-3 d-flex flex-column text-center text-md-start">
          <label class="align-self-start" for="origen">Seleccione Destino:</label>
          <select id="destino" v-model="reserva.destino" class="select-limitado" data-cy="select-reserva-destino">
            <option value="">-- Destino --</option>
            <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
              {{ estacion.nombre }}
            </option>
          </select>
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Fecha de inicio -->
        <div class="col-md-6 col-12 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start">Fecha de Inicio:</label>
          <input v-model="reserva.inicio" type="date" class="form-control" placeholder="Introduzca fecha..."
            data-cy="fechaInicio" />
        </div>
        <!-- Hora de inicio -->
        <div class="col-md-6 col-12 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start">Hora de Inicio:</label>
          <input v-model="reserva.horaInicio" type="time" class="form-control" placeholder="Introduzca hora..."
            data-cy="horaInicio" />
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Fecha de fin -->
        <div class="col-md-6 col-12 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start">Fecha de Fin:</label>
          <input v-model="reserva.fin" type="date" class="form-control" placeholder="Introduzca fecha..."
            data-cy="fechaFin" />
        </div>
        <!-- Hora de fin -->
        <div class="col-md-6 col-12 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start">Hora de Fin:</label>
          <input v-model="reserva.horaFin" type="time" class="form-control" placeholder="Introduzca hora..."
            data-cy="horaFin" />
        </div>
      </div>
      <!-- Botón para confirmar reserva -->
      <div class="row justify-content-center">
        <div class="col-auto">
          <button class="btn btn-primary" data-cy="reserva-boton">
            Realizar Reserva
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
defineOptions({
  name: "formulario-reserva",
});

const reserva = ref({
  inicio: "",
  horaInicio: "",
  fin: "",
  horaFin: "",
  origen: "",
  destino: "",
});

const emit = defineEmits(["reserva"]);

// Envía las condiciones de la reserva a la vista correspondiente para que formalice la reserva del usuario
const hacerReserva = () => {
  if (!reserva.value.origen || !reserva.value.destino) {
    alert("Por favor selecciona origen y destino");
    return;
  }
  emit("reserva", reserva.value);
};

const estaciones = ref([]);

// Obtiene el listado de estaciones para que el usuario pueda seleccionar la estación de origen y destino
const getEstaciones = async () => {
  try {
    // Realiza una solicitud GET para obtener las estaciones
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    // Guarda las estaciones disponibles
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
  max-width: 80%;
  text-overflow: ellipsis;
  border-radius: 10px;
  background-color: white;
}
</style>
