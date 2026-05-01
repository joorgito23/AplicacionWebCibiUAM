<!-- src/views/LeerNotificacionesView.vue -->
<template>
  <div id="notificaciones-view" class="notificaciones-view">
    <main>
      <h1 class="titulo-notificacion">
        Notificaciones de {{ authStore.usuario }}
      </h1>
      <p v-if="notificaciones === null" style="text-align: center">
        Obteniendo notificaciones...
      </p>
      <p v-else-if="notificaciones.length === 0" style="text-align: center; margin-left: 2rem; margin-right: 2rem">
        No dispones de notificaciones pendientes de lectura actualmente.
      </p>
      <div v-else class="row justify-content-center mt-3">
        <!-- Notificaciones del usuario sin leer -->
        <div class="col-11 col-md-8 d-flex justify-content-center mb-2">
          <div style="width: 100%">
            <div class="card card-cibiuam">
              <h2 class="titulo-tarjeta">
                <img src="/correo-electronico.png" alt="Info" class="icono" />
                Notificaciones sin leer
              </h2>
              <div class="info" v-for="noti in notificaciones" :key="noti.id">
                <span>
                  <div class="fecha">📅 Fecha: {{ noti.fecha }}</div>
                  <div class="contenido">✉️ {{ noti.msg }}</div>
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
defineOptions({ name: "notificaciones-view" });
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const notificaciones = ref(null);

// Función que obtiene las notificaciones del usuario
const getNotificaciones = async () => {
  try {
    // Realiza una solicitud GET a la API para obtener las notificaciones pendientes de lectura
    const response = await fetch(myVar + "/cibiuam/leer_notificaciones/", {
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

    // Guarda las notificaciones para msotrar
    const data = await response.json();
    notificaciones.value = data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getNotificaciones();
});
</script>

<style scoped>
.notificaciones-view {
  width: 100%;
}

.titulo-notificacion {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  margin-left: 1rem;
  margin-right: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
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

.titulo-tarjeta {
  margin-bottom: 20px;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 2rem;
  font-size: 16px;
  color: #475569;
}

@media (min-width: 768px) {
  .info {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 2rem;
    font-size: 18px;
    color: #475569;
  }
}

.info span {
  background: #eff6ff;
  border-radius: 6px;
  padding: 10px 5px;
  line-height: 1.8;
  text-align: center;
}

.fecha {
  text-align: center;
  color: rgb(49, 49, 49);
}

.contenido {
  text-align: left;
  color: rgb(49, 49, 49);
}

.icono {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.25rem;
}
</style>
