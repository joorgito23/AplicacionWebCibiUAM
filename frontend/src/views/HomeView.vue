<!-- src/views/HomeView.vue-->
<template>
  <div id="home-view">
    <main>
      <h1 class="home-title">¡Bienvenido a CibiUAM!</h1>
      <div class="row justify-content-center mt-3">
        <!-- Definición de CibiUAM-->
        <div class="col-11 col-lg-5 mb-4 d-flex justify-content-center mb-2">
          <div class="card border-3 rounded-4 p-2 card-cibiuam">
            <h2 class="titulo text-center mb-3">¿Qué es CibiUAM?</h2>
            <p class="definicion">
              El Centro Integral de la Bicicleta de la Universidad Autónoma de
              Madrid pretende fomentar el uso de este vehículo como medio de
              transporte cotidiano y sensibilizar sobre la necesidad de
              practicar una movilidad más sostenible, permitiendo reservar una
              bicicleta de manera rápida y sencilla para los desplazamientos en
              el campus de la UAM. Puede consultar el blog oficial de CibiUAM en
              el siguiente
              <a href="https://cibiuam.blogspot.com/p/que-es-el-cibiuam.html">enlace</a>.
            </p>
            <div class="text-center mt-2">
              <img src="/cibiuam.png" alt="Logo CibiUAM" class="img-fluid logo-cibiuam" />
            </div>
          </div>
        </div>
        <!-- Tarifas Disponibles-->
        <div class="col-11 col-lg-5 d-flex justify-content-center mb-2">
          <div class="card border-3 rounded-4 p-2 card-cibiuam">
            <h2 class="titulo text-center mb-3">
              ¿Aún no conoces nuestras tarifas?
            </h2>
            <div v-if="!tarifaSeleccionada" class="text-center my-4">
              <p>Cargando tarifas...</p>
            </div>
            <div v-else class="sub-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <button class="btn-flecha" @click="anterior">◀</button>
                <h3 class="titulo text-center mb-3">
                  <img src="/informacion.png" alt="Info" class="icono-titulo" />
                  Tarifa {{ tarifaSeleccionada.duracion }}
                </h3>
                <button class="btn-flecha" @click="siguiente" data-cy="siguiente">
                  ▶
                </button>
              </div>
              <div class="info">
                <span>
                  <strong>⌛ Duración: </strong>
                  <span class="detalle">
                    {{
                      tarifaSeleccionada.duracion.charAt(0).toUpperCase() +
                      tarifaSeleccionada.duracion.slice(1)
                    }}</span>
                </span>
                <span>
                  <strong>📝 Descripción: </strong>
                  <span class="detalle">
                    {{ tarifaSeleccionada.descripcion }}</span>
                </span>
                <span>
                  <strong><img src="/euro.png" alt="Euro" class="icono" /> Importe:
                  </strong>
                  <span class="detalle">
                    {{ tarifaSeleccionada.importe }}€</span>
                </span>
                <span>
                  <strong><img src="/tarifa-por-hora.png" alt="Euro" class="icono" />
                    Precio por minuto:
                  </strong>
                  <span class="detalle">
                    {{ tarifaSeleccionada.precioMinuto }}€</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: "home-view" });
import { ref, onMounted } from "vue";
const myVar = import.meta.env.VITE_DJANGOURL;
const tarifas = ref([]);
const datosTarifas = ref([]);
const tarifaSeleccionada = ref(null);
const mensajeError = ref("");
const indiceActual = ref(0);

// Función que obtiene las tarifas existentes de la aplicación y su información detallada
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

    // Guardamos las tarifas disponibles para mostrar
    const data = await response.json();
    tarifas.value = data;
  } catch (error) {
    console.error(error);
  }

  // Obtiene la información detallada de cada tarifa disponible
  for (let i = 0; i < tarifas.value.length; i++) {
    try {
      const datos = { nombre: tarifas.value[i].duracion };
      // Realiza una solicitud POST para obtener los detalles de la tarifa
      const response1 = await fetch(myVar + "/cibiuam/consultar_tarifa/", {
        method: "POST",
        body: JSON.stringify(datos),
        headers: { "Content-type": "application/json; charset=UTF-8" },
      });

      if (!response1.ok) {
        const errorData = await response1.json();
        console.error("Error:", errorData);
        return;
      }

      // Guardamos la información detallada de cada tarifa para mostrar
      const data1 = await response1.json();
      if (i === 0) {
        tarifaSeleccionada.value = data1;
      }
      datosTarifas.value.push(data1);
    } catch (error) {
      console.error(error);
    }
  }
};

// Función para mostrar la siguiente tarifa disponible al usuario
const siguiente = () => {
  if (datosTarifas.value.length === 0) return;
  indiceActual.value = (indiceActual.value + 1) % datosTarifas.value.length;
  tarifaSeleccionada.value = datosTarifas.value[indiceActual.value];
};

// Función para mostrar la anterior tarifa al usuario
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
</script>

<style scoped>
.home-title {
  text-align: center;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
  margin-top: 1rem;
}

.card-cibiuam {
  background: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-cibiuam:hover {
  transform: translateY(-5px);
}

.titulo {
  text-align: center;
  margin-top: 2rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.definicion {
  text-align: justify;
  margin-top: 1rem;
  margin-left: 1rem;
  margin-right: 1rem;
}

.logo-cibiuam {
  width: 50%;
}

.sub-card {
  background: white;
  border-radius: 12px;
  border: 2px solid green;
  padding: 24px 12px;
  width: 90%;
  text-align: center;
  border-top: 7px solid green;
  overflow: hidden;
  margin: 20px auto;
}

.btn-flecha {
  background: green;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
}

.btn-flecha:hover {
  background: green;
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
