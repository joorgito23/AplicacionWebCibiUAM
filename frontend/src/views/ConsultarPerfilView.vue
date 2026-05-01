<!-- src/views/ConsultarPerfilView.vue -->
<template>
  <div id="consultar-perfil-view" class="consultar-perfil-view">
    <main>
      <div class="row justify-content-center mt-3">
        <!-- Datos personales del usuario -->
        <div class="col-11 col-lg-4 col-md-8 justify-content-center mb-2">
          <div class="card card-cibiuam">
            <h1 class="titulo-perfil" data-cy="titulo-perfil">
              Perfil del Usuario
            </h1>
            <div v-if="perfil" class="info">
              <span class="fondo"><strong><img src="/carne-de-identidad.png" alt="Id" class="icono" />
                  Nombre de Usuario: </strong>
                <span class="detalles">{{ perfil.usuario }}</span></span>
              <span class="fondo"><strong><img src="/user.png" alt="Nombre Apellidos" class="icono" />
                  Nombre y Apellidos: </strong>
                <span class="detalles">{{ perfil.nombre }} {{ perfil.apellidos }}</span></span>
              <span class="fondo"><strong><img src="/coordinar.png" alt="Rol" class="icono" />
                  Rol: </strong>
                <span class="detalles">{{ perfil.rol }}</span></span>
              <span class="fondo"><strong><img src="/tarifas-de-cajeros-automaticos.png" alt="Tarifa" class="icono" />
                  Tarifa Actual: </strong>
                <span class="detalles">{{ perfil.duracion }}</span></span>
              <span class="fondo"><strong><img src="/caducado.png" alt="Fin" class="icono" />
                  Finalización Contrato Actual: </strong>
                <span class="detalles">{{ perfil.fin }}</span></span>
              <span class="fondo"><strong><img src="/billete-de-banco.png" alt="Euro" class="icono" />
                  Saldo Disponible: </strong>
                <span class="detalles">{{ perfil.saldo }}€</span></span>
              <span class="fondo">
                <strong><img src="/llamar.png" alt="Tlf" class="icono" />
                  Teléfono: </strong>
                <input style="border-radius: 12px; margin-left: 1rem" id="tlf" type="text" v-model="perfil.tlf"
                  class="detalles" data-cy="input-tlf" />
              </span>
            </div>
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success">{{ mensaje }}</p>
              </div>
              <div v-if="mensajeError">
                <p class="alert alert-danger">{{ mensajeError }}</p>
              </div>
            </div>
            <!-- Botón de actualización de datos personales -->
            <div class="contenedor-boton">
              <button class="btn btn-primary" @click="actualizarPerfil" data-cy="act-tlf">
                Actualizar Perfil
              </button>
            </div>
          </div>
        </div>
        <!-- Cambio de contraseña -->
        <div class="col-11 col-lg-4 col-md-8 justify-content-center mb-2">
          <div class="card card-cibiuam">
            <h1 class="titulo-perfil" data-cy="titulo-password">
              Cambio de Contraseña
            </h1>
            <div v-if="perfil" class="info">
              <span class="fondo">
                <strong>Contraseña Actual: </strong>
                <div class="contenedor-password">
                  <input style="border-radius: 12px" id="passActual" :type="mostrarPassword ? 'text' : 'password'"
                    v-model="cambio.antigua" class="detalles" data-cy="input-pass-antigua"
                    placeholder="Escribe aquí..." />
                  <img :src="mostrarPassword ? '/invisible.png' : '/ojo.png'" class="visible"
                    @click="mostrarPassword = !mostrarPassword" alt="Mostrar / Ocultar contraseña" />
                </div>
              </span>
              <span class="fondo">
                <strong>Nueva Contraseña: </strong>
                <div class="contenedor-password">
                  <input style="border-radius: 12px" id="passNueva" :type="mostrarPassword2 ? 'text' : 'password'"
                    v-model="cambio.nueva" class="detalles" data-cy="input-pass-nueva" placeholder="Escribe aquí..." />
                  <img :src="mostrarPassword2 ? '/invisible.png' : '/ojo.png'" class="visible"
                    @click="mostrarPassword2 = !mostrarPassword2" alt="Mostrar / Ocultar contraseña" />
                </div>
              </span>
              <span class="fondo">
                <strong>Repita Nueva Contraseña: </strong>
                <div class="contenedor-password">
                  <input style="border-radius: 12px" id="passNueva2" :type="mostrarPassword3 ? 'text' : 'password'"
                    v-model="cambio.nueva2" class="detalles" data-cy="input-pass-nueva2"
                    placeholder="Escribe aquí..." />
                  <img :src="mostrarPassword3 ? '/invisible.png' : '/ojo.png'" class="visible"
                    @click="mostrarPassword3 = !mostrarPassword3" alt="Mostrar / Ocultar contraseña" />
                </div>
              </span>
            </div>
            <div class="contenedor">
              <div v-if="mensajeCambio">
                <p class="alert alert-success">{{ mensajeCambio }}</p>
              </div>
              <div v-if="mensajeErrorCambio">
                <p class="alert alert-danger">{{ mensajeErrorCambio }}</p>
              </div>
            </div>
            <!-- Botón de actualización de contraseña -->
            <div class="contenedor-boton">
              <button class="btn btn-primary" @click="actualizarContraseña" data-cy="act-pass">
                Actualizar Contraseña
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: "consultar-perfil-view" });
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const perfil = ref(null);

// Variable para mostrar o no la contraseña
const mostrarPassword = ref(false);
const mostrarPassword2 = ref(false);
const mostrarPassword3 = ref(false);

// Función que obtiene los datos personales del usuario para mostrarlos por pantalla
const getPerfil = async () => {
  try {
    // Realiza una solicitud GET a la API para obtener el perfil del usuario
    const response = await fetch(myVar + "/cibiuam/consultar_perfil/", {
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

    // Guarda los datos del usuario
    const data = await response.json();
    perfil.value = data;
  } catch (error) {
    console.error(error);
  }
};
const mensaje = ref("");
const mensajeError = ref("");

// Función que actualiza el número de teléfono del usuario
const actualizarPerfil = async () => {
  try {
    // Realiza una solicitud POST a la API para actualizar el número de teléfono
    const nuevoTlf = perfil.value.tlf;
    const response = await fetch(myVar + "/cibiuam/modificar_perfil/", {
      method: "POST",
      body: JSON.stringify({ tlf: nuevoTlf }),
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
      }, 3000);
      return;
    }

    const data = await response.json();
    mensaje.value = data.Mensaje;
    setTimeout(() => {
      mensaje.value = "";
    }, 3000);
  } catch (error) {
    console.error(error);
  }
};

const mensajeCambio = ref("");
const mensajeErrorCambio = ref("");
const cambio = ref({
  antigua: "",
  nueva: "",
  nueva2: "",
});

// Función que actualiza la contraseña del usuario
const actualizarContraseña = async () => {
  if (
    !cambio.value.nueva.trim() ||
    !cambio.value.antigua.trim() ||
    !cambio.value.nueva2.trim()
  ) {
    alert("Introduzca ambas contraseñas");
    return;
  }

  if (cambio.value.nueva !== cambio.value.nueva2) {
    mensajeErrorCambio.value = "Las contraseñas no coinciden.";
    setTimeout(() => {
      mensajeErrorCambio.value = "";
    }, 3000);

    return;
  }

  try {
    // Realiza una solicitud POST a la API para actualizar la contraseña
    const nuevaPassword = {
      current_password: cambio.value.antigua,
      new_password: cambio.value.nueva,
    };
    const response1 = await fetch(myVar + "/auth/users/set_password/", {
      method: "POST",
      body: JSON.stringify(nuevaPassword),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response1.ok) {
      const errorData = await response1.json();
      console.error("Error:", errorData);
      if (errorData.current_password) {
        mensajeErrorCambio.value = "La contraseña actual no es correcta.";
      } else {
        mensajeErrorCambio.value =
          "La nueva contraseña no es lo suficientemente segura.";
      }

      setTimeout(() => {
        mensajeErrorCambio.value = "";
      }, 3000);
      return;
    }

    mensajeCambio.value = "Contraseña cambiada correctamente.";
    setTimeout(() => {
      mensajeCambio.value = "";
    }, 3000);
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getPerfil();
});
</script>

<style scoped>
.consultar-perfil-view {
  width: 100%;
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

.titulo-perfil {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
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

.info span.fondo {
  background: #eff6ff;
  border-radius: 6px;
  padding: 10px 26px;
  line-height: 1.8;
  display: block;
  text-align: left;
}

.detalles {
  color: black;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 0.5rem;
}

.contenedor-boton {
  width: 100%;
  margin-top: 0.5rem;
}

.btn-primary {
  margin: 10px;
  font-size: 19px;
  background-color: green !important;
  border-color: black !important;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}

.contenedor-password {
  position: relative;
  display: inline-block;
}

.contenedor-password input {
  padding-right: 40px;
}

.visible {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  width: 20px;
  height: 20px;
  object-fit: contain;
  background-color: transparent;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
  margin-right: 0.5rem;
}
</style>
