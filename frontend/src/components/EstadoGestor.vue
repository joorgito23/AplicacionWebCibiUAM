<!-- src/components/EstadoGestor.vue -->
<template>
  <div id="estado-gestor-componente">
    <div class="row justify-content-center mt-3">
      <div class="col-11 col-md-10 d-flex justify-content-center mb-2">
        <div class="card border-2 rounded-4 p-2 card-cibiuam w-100">
          <h2 class="def text-center mb-3">Estado actual de las bicicletas</h2>
          <div v-if="!biciSeleccionada" class="text-center my-4">
            <p>Cargando bicicletas...</p>
          </div>
          <!-- Estado de cada bicicleta -->
          <div v-else class="sub-card">
            <!-- Flechas para cambiar de bicicleta a consultar -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <button class="btn-flecha" @click="anterior" data-cy="anteriorBici">
                ◀
              </button>
              <h3 class="def text-center mb-3">
                🚴 Bicicleta con id {{ biciSeleccionada.id }}
              </h3>
              <button class="btn-flecha" @click="siguiente" data-cy="sig">
                ▶
              </button>
            </div>
            <!-- Información del estado actual-->
            <div class="info">
              <span><strong><img src="/mapaUbi.png" alt="Ubic" class="icono-titulo" />
                  Estado: </strong>{{ biciSeleccionada.estado }}</span>
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
defineOptions({ name: "estado-gestor-componente" });
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();
const myVar = import.meta.env.VITE_DJANGOURL;

const bicicletas = ref([]);
const biciSeleccionada = ref("");
const estadoBicicletas = ref([]);
const indiceActual = ref(0);
const hora = ref(null);

// Función para obtener el estado de las bicicletas del campus
const getBicicletas = async () => {
  try {
    // Realiza una solicitud GET para obtener las bicicletas
    const response = await fetch(myVar + "/cibiuam/informacion/bicicletas/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    // Guarda las bicicletas existentes
    const data = await response.json();
    bicicletas.value = data;
  } catch (error) {
    console.error(error);
  }

  // Consulta el estado de cada bicicleta
  for (let i = 0; i < bicicletas.value.length; i++) {
    try {
      const datos = { id: bicicletas.value[i].id };
      // Realiza una solicitud POST para obtener el estado de la bicicleta
      const response = await fetch(
        myVar + "/cibiuam/consultar_estado_bicicleta/",
        {
          method: "POST",
          body: JSON.stringify(datos),
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + authStore.token,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        return;
      }

      const data = await response.json();
      const nuevaBici = {
        id: bicicletas.value[i].id,
        estado: data.Mensaje,
      };
      estadoBicicletas.value.push(nuevaBici);
      hora.value = new Date().toLocaleTimeString();
      if (i === 0) {
        biciSeleccionada.value = nuevaBici;
      }
    } catch (error) {
      console.error(error);
    }
  }
};

// Función para mostrar el estado de la siguiente bicicleta
const siguiente = () => {
  if (estadoBicicletas.value.length === 0) return;
  indiceActual.value = (indiceActual.value + 1) % estadoBicicletas.value.length;
  biciSeleccionada.value = estadoBicicletas.value[indiceActual.value];
};

// Función para mostrar el estado de la anterior bicicleta
const anterior = () => {
  if (estadoBicicletas.value.length === 0) return;
  indiceActual.value =
    (indiceActual.value - 1 + estadoBicicletas.value.length) %
    estadoBicicletas.value.length;
  biciSeleccionada.value = estadoBicicletas.value[indiceActual.value];
};

onMounted(() => {
  getBicicletas();
});
</script>

<style scoped>
.card-cibiuam {
  background: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-cibiuam:hover {
  transform: translateY(-5px);
}

.def {
  text-align: center;
  margin-top: 2rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
  margin-right: 0.1rem;
  margin-left: 0.1rem;
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

.icono-titulo {
  width: 25px;
  height: 25px;
  vertical-align: middle;
  margin-right: 0.5rem;
}
</style>
