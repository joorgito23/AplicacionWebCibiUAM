<!-- src/components/FiltrosReservas.vue -->
<template>
  <div id="filtro-reserva">
    <div class="filtros-panel">
      <div class="filtros-grid">
        <!-- Origen -->
        <div class="filtro-grupo">
          <label class="filtro-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            Origen
          </label>
          <select v-model="filtros.origen" class="filtro-select" data-cy="select-reserva-origen">
            <option value="">Todas las estaciones</option>
            <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
              {{ estacion.nombre }}
            </option>
          </select>
        </div>
        <!-- Destino -->
        <div class="filtro-grupo">
          <label class="filtro-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            Destino
          </label>
          <select v-model="filtros.destino" class="filtro-select" data-cy="select-reserva-destino">
            <option value="">Todas las estaciones</option>
            <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
              {{ estacion.nombre }}
            </option>
          </select>
        </div>
        <!-- Fecha inicio -->
        <div class="filtro-grupo">
          <label class="filtro-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            Fecha inicio
          </label>
          <input type="date" v-model="filtros.inicio" class="filtro-input" data-cy="inicio" />
        </div>
        <!-- Fecha fin -->
        <div class="filtro-grupo">
          <label class="filtro-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            Fecha fin
          </label>
          <input type="date" v-model="filtros.fin" class="filtro-input" data-cy="fin" />
        </div>
      </div>
      <div class="filtros-footer">
        <button class="btn-limpiar" @click="limpiarFiltros">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" />
          </svg>
          Limpiar
        </button>
        <button class="btn-filtrar" @click="filtrarReservas" data-cy="filtrar-boton">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
          </svg>
          Filtrar reservas
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "filtro-reserva" });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const mensajeError = ref("");
const filtros = ref({
  origen: "",
  destino: "",
  inicio: "",
  fin: "",
});

const emit = defineEmits(["filtrar-reservas"]);

//Función para enviar los filtros deseados por el usuario a la vista correspondiente
const filtrarReservas = async () => {
  emit("filtrar-reservas", filtros.value);
};

const estaciones = ref([]);
// Función para obtener las estaciones registradas en la aplicación
const getEstaciones = async () => {
  try {
    // Realiza una solicitud GET para obtener las estaciones disponibles
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

// Función que limpia los filtros establecidos
const limpiarFiltros = () => {
  filtros.value.origen = "";
  filtros.value.destino = "";
  filtros.value.inicio = "";
  filtros.value.fin = "";
};
</script>

<style scoped>
.filtros-panel {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.5rem;
  max-width: 1280px;
  margin: 2rem auto 0;
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 1rem;
}

.filtro-grupo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filtro-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  font-weight: 600;
  color: #000000;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.filtro-label svg {
  color: #000000;
}

.filtro-select,
.filtro-input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 16px;
  color: #1f2937;
  background: #f9fafb;
  transition: border-color 0.2s ease, background 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  outline: none;
  font-family: "Playfair Display", serif;
}

.filtro-select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239ca3af' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

.filtro-select:focus,
.filtro-input:focus {
  border-color: #4a7729;
  background: white;
}

.filtro-select:hover,
.filtro-input:hover {
  border-color: #d1d5db;
  background: white;
}

.filtros-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid #f3f4f6;
}

.btn-filtrar {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 20px;
  background: #4a7729;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease;
  font-family: "Playfair Display", serif;
}

.btn-filtrar:hover {
  background: #0077c8;
  transform: translateY(-1px);
}

.btn-filtrar:active {
  transform: translateY(0);
}

.btn-limpiar {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 16px;
  background: transparent;
  color: #000000;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: "Playfair Display", serif;
}

.btn-limpiar:hover {
  background: #f9fafb;
  color: #000000;
  border-color: #d1d5db;
}

@media (max-width: 576px) {
  .filtros-panel {
    margin: 1rem 0.75rem 0;
    padding: 1.25rem;
  }

  .filtros-grid {
    grid-template-columns: 1fr;
  }

  .filtros-footer {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .btn-filtrar,
  .btn-limpiar {
    justify-content: center;
  }
}
</style>
