<!-- src/components/EstadoCampus.vue-->
<template>
  <div id="estado-componente">
    <div class="row justify-content-center mt-3">
      <div class="col-11 col-md-10 d-flex justify-content-center mb-2">
        <div class="card border-2 rounded-4 p-2 card-cibiuam w-100">
          <h2 class="titulo text-center mb-3">
            Estado actual de las estaciones
          </h2>
          <div v-if="!estacionSeleccionada" class="text-center my-4">
            <p>Cargando estaciones...</p>
          </div>
          <!-- Estado actual de cada estación -->
          <div v-else class="sub-card">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <button class="btn-flecha" @click="anterior" data-cy="anterior">
                ◀
              </button>
              <h3 class="titulo text-center mb-3">
                <img src="/parking-de-bicicletas.png" alt="Parking" class="icono-titulo" />
                Estación {{ estacionSeleccionada.nombre }}
              </h3>
              <button class="btn-flecha" @click="siguiente" data-cy="siguienteEst">
                ▶
              </button>
            </div>
            <div class="info">
              <span><strong><img src="/ubic.png" alt="Ubic" class="icono-titulo" />
                  Ubicación: </strong><span class="detalle">{{
                    estacionSeleccionada.ubicacion
                  }}</span></span>
              <span><img src="/bicicleta.png" alt="Bici" class="icono-titulo" />
                <strong>Bicicletas disponibles: </strong><span class="detalle">{{
                  estacionSeleccionada.ocupado
                  }}</span></span>
              <span><img src="/anc.png" alt="Anclaje" class="icono-titulo" />
                <strong>Anclajes libres: </strong><span class="detalle">{{
                  estacionSeleccionada.libre
                  }}</span></span>
            </div>
            <div class="footer">
              🕒 Actualizado: <span>{{ hora }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "estado-componente" });
import { ref, onMounted, watch } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const estaciones = ref([]);
const datosEstaciones = ref([]);
const estacionSeleccionada = ref(null);
const mensajeError = ref("");
const indiceActual = ref(0);
const hora = ref(null);
const emit = defineEmits(["marcar"]);
const envio = ref(null);

// Función que obtiene las estaciones del campus
const getEstaciones = async () => {
  try {
    // Realiza una solicitud GET para obtener las estaciones
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = "Error al obtener informacion de las estaciones";
      return;
    }

    const data = await response.json();

    // Guarda las estaciones para mostrar
    estaciones.value = data;
  } catch (error) {
    console.error(error);
  }

  // Consulta el estado actual de cada estación
  for (let i = 0; i < estaciones.value.length; i++) {
    try {
      const datos = { estacion: estaciones.value[i].nombre };
      // Realiza una solicitud POST a la API para consultar el estado
      const response = await fetch(myVar + "/cibiuam/consultar_estado/", {
        method: "POST",
        body: JSON.stringify(datos),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        mensajeError.value = errorData.Mensaje;
        return;
      }

      // Guarda el estado de la estación para mostrar la información en tiempo real
      const data = await response.json();
      const nuevaEst = {
        nombre: estaciones.value[i].nombre,
        ubicacion: estaciones.value[i].ubicacion,
        libre: data.libre,
        ocupado: data.ocupado,
      };
      datosEstaciones.value.push(nuevaEst);
      hora.value = new Date().toLocaleTimeString();
      if (i === 0) {
        estacionSeleccionada.value = nuevaEst;
      }
    } catch (error) {
      console.error(error);
    }
  }
};

// Función para consultar el estado de la siguiente estación
const siguiente = () => {
  if (datosEstaciones.value.length === 0) return;
  indiceActual.value = (indiceActual.value + 1) % datosEstaciones.value.length;
  estacionSeleccionada.value = datosEstaciones.value[indiceActual.value];
  envio.value = estaciones.value[indiceActual.value];
  emit("marcar", envio.value);
};

// Función para consultar el estado de la anterior estación
const anterior = () => {
  if (datosEstaciones.value.length === 0) return;
  indiceActual.value =
    (indiceActual.value - 1 + datosEstaciones.value.length) %
    datosEstaciones.value.length;
  estacionSeleccionada.value = datosEstaciones.value[indiceActual.value];
  envio.value = estaciones.value[indiceActual.value];
  emit("marcar", envio.value);
};

const props = defineProps({
  estacionEstado: {
    type: String,
    default: null,
  },
});

// Monitoriza clicks del usuario en el mapa para mostrar el estado de la estación marcada en el mapa
watch(
  () => props.estacionEstado,
  (nuevaEstacionMostrada) => {
    if (nuevaEstacionMostrada) {
      for (let i = 0; i < estaciones.value.length; i++) {
        if (estaciones.value[i].nombre === nuevaEstacionMostrada) {
          indiceActual.value = i;
          estacionSeleccionada.value =
            datosEstaciones.value[indiceActual.value];
          break;
        }
      }
    }
  },
  { immediate: true }
);

onMounted(() => {
  getEstaciones();
});
</script>

<style scoped>
.card-cibiuam {
  background: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-cibiuam:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.titulo {
  text-align: center;
  margin-top: 2rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
  margin-right: 0.1rem;
  margin-left: 0.1rem;
}

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.5rem;
}

.sub-card {
  background: white;
  border-radius: 12px;
  border: 2px solid #0b6f0d;
  padding: 24px 12px;
  width: 90%;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 20px auto;
}

.btn-flecha {
  background: #0b6f0d;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
}

.btn-flecha:hover {
  background: #166534;
  transform: scale(1.05);
}

.info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 16px;
  color: rgb(52, 52, 52);
}

@media (min-width: 768px) {
  .info {
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 18px;
    color: rgb(52, 52, 52);
  }
}

.info span {
  background: #eff6ff;
  border-radius: 6px;
  padding: 10px 1px;
  line-height: 1.8;
}

.detalle {
  color: black;
}

.footer {
  margin-top: 14px;
  font-size: 14px;
  color: black;
}
</style>
