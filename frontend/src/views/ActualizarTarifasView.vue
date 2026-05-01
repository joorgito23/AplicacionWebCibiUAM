<!-- src/views/ActualizarTarifasView.vue -->
<template>
  <div id="act-tarifa-view">
    <main>
      <h1 class="titulo-tarifa">Gestión de Tarifas CibiUAM</h1>
      <div class="row justify-content-center mt-3">
        <div class="col-11 col-lg-5 d-flex justify-content-center mb-2">
          <!-- Información de la tarifa-->
          <div class="card border-2 rounded-4 p-2 w-100">
            <h2 class="titulo text-center mb-3">
              <img src="/informacion.png" alt="Info" class="icono-titulo" />
              Detalles de las tarifas
            </h2>
            <div v-if="!tarifaSeleccionada" class="text-center my-4">
              <p>Cargando tarifas...</p>
            </div>
            <div v-else class="sub-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <button class="btn-flecha" @click="anterior">◀</button>
                <h3 class="titulo text-center mb-3">
                  Tarifa {{ tarifaSeleccionada.duracion }}
                </h3>
                <button class="btn-flecha" @click="siguiente" data-cy="siguiente-tarifa">
                  ▶
                </button>
              </div>
              <div class="info">
                <span>
                  <strong>⌛ Duración: </strong>
                  <span class="detalles">
                    {{
                      tarifaSeleccionada.duracion.charAt(0).toUpperCase() +
                      tarifaSeleccionada.duracion.slice(1)
                    }}</span>
                </span>
                <span>
                  <strong>📝 Descripción: </strong>
                  <span class="detalles">
                    {{ tarifaSeleccionada.descripcion }}</span>
                </span>
                <span>
                  <strong><img src="/euro.png" alt="Euro" class="icono" /> Importe:
                  </strong>
                  <span class="detalles">
                    {{ tarifaSeleccionada.importe }}€</span>
                </span>
                <span>
                  <strong><img src="/tarifa-por-hora.png" alt="Euro" class="icono" />
                    Precio por minuto:
                  </strong>
                  <span class="detalles">
                    {{ tarifaSeleccionada.precioMinuto }}€</span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <!-- Actualización de la tarifa -->
        <div class="col-11 col-lg-5 d-flex justify-content-center mb-2">
          <div class="card border-2 rounded-4 p-2 w-100">
            <h2 class="titulo text-center mb-3">🔄 Actualización de precios</h2>
            <div v-if="!tarifaSeleccionada" class="text-center my-4">
              <p>Cargando tarifas...</p>
            </div>
            <div v-else class="sub-card">
              <div class="d-flex justify-content-center align-items-center mb-3">
                <h3 class="titulo text-center mb-3">
                  Está usted actualizando la tarifa
                  {{ tarifaSeleccionada.duracion }}
                </h3>
              </div>
              <div class="info">
                <span>
                  <strong><img src="/euro.png" alt="Euro" class="icono" /> Nuevo
                    Importe:</strong>
                  <input style="
                      margin-left: 1rem;
                      border-radius: 10px;
                      border-color: black;
                    " id="importe" type="number" v-model="importe" step="0.01" class="detalles" data-cy="n-imp"
                    placeholder="Introduzca nuevo importe..." />
                </span>
                <span>
                  <strong><img src="/tarifa-por-hora.png" alt="Euro" class="icono" />
                    Nuevo Precio por Minuto:</strong>
                  <input style="
                      margin-left: 1rem;
                      border-radius: 10px;
                      border-color: black;
                    " id="precioMinuto" type="number" v-model="precioMinuto" step="0.01" class="detalles"
                    data-cy="n-pm" placeholder="Introduzca nuevo precio..." />
                </span>
              </div>
              <button class="btn btn-primary" @click="actualizarTarifa" data-cy="act-tar">
                Actualizar Tarifa
              </button>
            </div>
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success">{{ mensaje }}</p>
              </div>
              <div v-if="mensajeError">
                <p class="alert alert-danger">{{ mensajeError }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { ref, onMounted } from "vue";

defineOptions({ name: "tarifa-view" });

const authStore = useAuthStore();
const myVar = import.meta.env.VITE_DJANGOURL;
const mensaje = ref("");
const tarifas = ref([]);
const datosTarifas = ref([]);
const tarifaSeleccionada = ref(null);
const mensajeError = ref("");
const indiceActual = ref(0);

// Función para obtener las tarifas disponibles
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

    // Guarda las tarifas existentes
    const data = await response.json();
    tarifas.value = data;
  } catch (error) {
    console.error(error);
  }

  // Obtiene los detalles de cada tarifa
  for (let i = 0; i < tarifas.value.length; i++) {
    try {
      const datos = { nombre: tarifas.value[i].duracion };
      // Realiza una solicitud POST a la API para obtener los detalles de cada tarifa
      const response = await fetch(myVar + "/cibiuam/consultar_tarifa/", {
        method: "POST",
        body: JSON.stringify(datos),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        return;
      }

      const data = await response.json();
      if (i === 0) {
        tarifaSeleccionada.value = data;
      }
      datosTarifas.value.push(data);
    } catch (error) {
      console.error(error);
    }
  }
};

// Función para cambiar a la siguiente tarifa
const siguiente = () => {
  if (datosTarifas.value.length === 0) return;
  indiceActual.value = (indiceActual.value + 1) % datosTarifas.value.length;
  tarifaSeleccionada.value = datosTarifas.value[indiceActual.value];
};

// Función para cambiar a la tarifa anterior
const anterior = () => {
  if (datosTarifas.value.length === 0) return;
  indiceActual.value =
    (indiceActual.value - 1 + datosTarifas.value.length) %
    datosTarifas.value.length;
  tarifaSeleccionada.value = datosTarifas.value[indiceActual.value];
};

onMounted(() => {
  getTarifas();
});

const importe = ref(null);
const precioMinuto = ref(null);

// Función que actualiza la tarifa deseada
const actualizarTarifa = async () => {
  if (!importe.value && !precioMinuto.value) {
    mensajeError.value =
      "Debe indicar el nuevo importe o precio por minuto deseado";
    setTimeout(() => {
      mensajeError.value = "";
    }, 3000);
    return;
  }

  try {
    const datos1 = { nombre: tarifaSeleccionada.value.duracion };
    if (importe.value) {
      datos1.importe = importe.value;
    }
    if (precioMinuto.value) {
      datos1.precioMinuto = precioMinuto.value;
    }

    // Realiza una solicitud POST a la API para actualizar la tarifa seleccionada
    const response1 = await fetch(myVar + "/cibiuam/actualizar_tarifa/", {
      method: "POST",
      body: JSON.stringify(datos1),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response1.ok) {
      const errorData = await response1.json();
      console.error("Error:", errorData);
      mensajeError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeError.value = "";
      }, 4000);
      return;
    } else {
      const resp = await response1.json();
      mensaje.value = resp.Mensaje;
      setTimeout(() => {
        mensaje.value = "";
      }, 4000);
    }

    try {
      const datos2 = { nombre: tarifaSeleccionada.value.duracion };
      // Realiza una solicitud POST para obtener las nuevas condiciones de la tarifa actualizada por el gestor
      const response2 = await fetch(myVar + "/cibiuam/consultar_tarifa/", {
        method: "POST",
        body: JSON.stringify(datos2),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      });

      if (!response2.ok) {
        const errorData = await response2.json();
        console.error("Error:", errorData);
        mensajeError.value = errorData.Mensaje;
        setTimeout(() => {
          mensajeError.value = "";
        }, 4000);
        return;
      }

      const nuevaTarifa = await response2.json();
      datosTarifas.value.splice(indiceActual.value, 1, nuevaTarifa);
      tarifaSeleccionada.value = datosTarifas.value[indiceActual.value];
    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.titulo-tarifa {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.titulo {
  text-align: center;
  margin-top: 2rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
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

.detalles {
  color: black;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
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

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.25rem;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
  margin-right: 0.25rem;
}
</style>
