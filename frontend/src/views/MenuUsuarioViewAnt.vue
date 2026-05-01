<!-- src/views/MenuUsuarioView.vue-->
<template>
  <div id="usuario-view">
    <main>
      <h1 class="titulo-usuario">
        ¡Bienvenido, {{ usuario }}!
        <span @click="mostrarAyuda = !mostrarAyuda" style="cursor: pointer">
          <img src="/ayuda.png" alt="Ayuda" class="icono" />
        </span>
      </h1>
      <div class="row justify-content-center">
        <div class="col-10 col-lg-6 d-flex justify-content-center">
          <p v-if="mostrarAyuda" class="instrucciones">
            En esta sección podrá visualizar todas las acciones que tiene
            permitidas como usuario de la aplicación CibiUAM. Para obtener más
            información acerca de una acción determinada acceda a su sección
            correspondiente.
          </p>
        </div>
      </div>
      <!-- Acciones del usuario-->
      <div class="row justify-content-center mb-lg-2">
        <!-- Estado del campus-->
        <div class="col-8 col-md-5 col-lg-3 mb-2 d-flex justify-content-center">
          <div class="card border-3 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/estadoImagen.png" alt="ConsultarEstado" class="imagen-accion img-fluid" />
            <router-link to="/consultar_estado" class="btn btn-primary mt-1 mx-auto" data-cy="estado-page">
              Consultar Estado del Campus
            </router-link>
          </div>
        </div>
        <div class="d-none d-lg-block col-lg-1"></div>
        <!-- Realizar reserva -->
        <div class="col-8 col-md-5 col-lg-3 mb-2 d-flex justify-content-center">
          <div class="card border-3 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/reservaImagen.png" alt="RealizarReserva" class="imagen-accion img-fluid" />
            <router-link to="/realizar_reserva" class="btn btn-primary mt-1 mx-auto" data-cy="reserva-page">
              Realizar Reserva
            </router-link>
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Cancelar reserva-->
        <div class="col-8 col-md-5 col-lg-3 mb-2 d-flex justify-content-center">
          <div class="card border-3 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/cancelarImagen.png" alt="cancelarReserva" class="imagen-accion img-fluid" />
            <router-link to="/cancelar_reserva" class="btn btn-primary mt-1 mx-auto" data-cy="cancelar-page">Cancelar
              Reserva</router-link>
          </div>
        </div>
        <div class="d-none d-lg-block col-lg-1"></div>
        <!-- Renovar contrato-->
        <div class="col-8 col-md-5 col-lg-3 mb-2 d-flex justify-content-center">
          <div class="card border-3 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/renovarImagen.png" alt="renovar" class="imagen-accion img-fluid" />
            <router-link to="/renovar_contrato" class="btn btn-primary mt-1 mx-auto" data-cy="renovar-page">Renovar
              Contrato</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
defineOptions({ name: "usuario-view" });
const authStore = useAuthStore();
const usuario = authStore.usuario;
const mostrarAyuda = ref(false);
</script>

<style scoped>
.titulo-usuario {
  text-align: center;
  margin-right: 0.15rem;
  margin-left: 0.15rem;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  padding: 0 1rem;
  margin-top: 0.5rem;
}

.accion {
  text-align: center;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
}

.imagen-accion {
  border-radius: 15px;
}

.btn-primary {
  margin: 0px;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
  width: 100%;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}
</style>
