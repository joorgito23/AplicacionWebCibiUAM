<!-- src/views/AltaBiciView.vue -->
<template>
  <div id="alta-bici-view" style="width: 100%">
    <main>
      <h1 class="titulo-alta-bici" data-cy="bici-title">Alta de Bicicleta</h1>
      <div class="row justify-content-center">
        <div class="col-11 col-lg-6 d-flex justify-content-center">
          <p class="instrucciones">
            Esta sección permite dar de alta una nueva bicicleta en el campus.
            Para ello, deberá introducir los campos solicitados en el formulario
            y, una vez validados, la bicicleta será asignada a la estación y
            anclaje deseado. Dicha bicicleta estará disponible para ser
            reservada desde el momento del alta.
          </p>
        </div>
      </div>
      <!-- Formulario de la bicicleta-->
      <div class="row justify-content-center">
        <div class="col-10 col-lg-8 d-flex justify-content-center">
          <div class="card card-cibiuam">
            <div class="row mb-3 justify-content-center">
              <div class="col-lg-12 col-12 d-flex flex-column justify-content-center mb-3">
                <h2 class="titulo text-center mb-3">
                  <img src="/bicicleta.png" alt="Bici" class="icono-titulo" />
                  Detalles de la Bicicleta
                </h2>
                <!-- Estación -->
                <label for="est" class="align-self-start me-2">Seleccione la estación deseada:</label>
                <select id="est" v-model="estacionSeleccionada" @change="mostrarAnclajes" class="select-limitado mb-3"
                  data-cy="select-est">
                  <option value="">-- Estación --</option>
                  <option v-for="estacion in estaciones" :key="estacion.nombre" :value="estacion.nombre">
                    {{ estacion.nombre }}
                  </option>
                </select>
                <!-- Número de anclaje-->
                <label for="anc" class="align-self-start me-2">Seleccione el número de anclaje deseado:</label>
                <select id="anc" v-model="anclajeSeleccionado" data-cy="select-anc" class="select-limitado">
                  <option value="">-- Anclaje --</option>
                  <option v-if="estacionSeleccionada && estacionMostrada !== null"
                    v-for="n in estacionMostrada.nAnclajes" :key="n" :value="n">
                    {{ n }}
                  </option>
                </select>
              </div>
            </div>
            <!-- Botón de alta-->
            <div class="row justify-content-center">
              <div class="col-auto">
                <button class="btn btn-primary" @click="altaBicicleta" data-cy="alta-bici-boton">
                  Dar de Alta
                </button>
              </div>
            </div>
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success" data-cy="msg">{{ mensaje }}</p>
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
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "alta-bici-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const router = useRouter();
const estaciones = ref([]);
const estacionSeleccionada = ref("");
const anclajeSeleccionado = ref("");

// Función que obtiene las estaciones del campus
const getEstaciones = async () => {
  try {
    // Realiza una solicitud GET para obtener las estaciones
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    const data = await response.json();
    // Guarda las estaciones existentes para mostrarlas al usuario
    estaciones.value = data;
  } catch (error) {
    console.error(error);
  }
};
const estacionMostrada = ref(null);

// Función para determinar la estación en la que el usuario desea dar de alta una bicicleta nueva
const mostrarAnclajes = async () => {
  if (!estacionSeleccionada.value) {
    return;
  }
  for (let i = 0; i < estaciones.value.length; i++) {
    if (estaciones.value[i].nombre == estacionSeleccionada.value) {
      estacionMostrada.value = estaciones.value[i];
      break;
    }
  }
};

const mensajeError = ref("");
const mensaje = ref("");

// Función que realiza el alta de una bicicleta
const altaBicicleta = async () => {
  if (
    !estacionSeleccionada.value ||
    !anclajeSeleccionado.value ||
    estacionSeleccionada.value === "" ||
    anclajeSeleccionado.value === ""
  ) {
    mensajeError.value = "Debe indicar todos los campos";
    setTimeout(() => {
      mensajeError.value = "";
    }, 3000);
    return;
  }

  try {
    const datos = {
      estacion: estacionSeleccionada.value,
      anclajeId: anclajeSeleccionado.value,
    };
    // Realiza una solicitud POST a la API para crear una nueva bicicleta
    const response = await fetch(myVar + "/cibiuam/alta_bicicleta/", {
      method: "POST",
      body: JSON.stringify(datos),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeError.value = "";
      }, 4000);
      return;
    }

    const data = await response.json();
    mensaje.value =
      data.Mensaje + " Serás redirigido automáticamente al menú inicial.";
    setTimeout(() => {
      router.push("/menu_gestor");
    }, 4000);
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getEstaciones();
});
</script>

<style scoped>
.titulo-alta-bici {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin: 0 auto 1rem auto;
  padding: 0 1rem;
}

.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 20px auto;
}

.titulo {
  text-align: center;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
}

.select-limitado {
  text-overflow: ellipsis;
  border-radius: 10px;
  background-color: white;
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

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
}

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.5rem;
}
</style>
