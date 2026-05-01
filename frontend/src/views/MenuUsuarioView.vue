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
      <div class="menu-grid">
        <!-- Consultar estado-->
        <router-link to="/consultar_estado" class="menu-card" data-cy="estado-page">
          <div class="menu-card-img">
            <img src="/estadoImagen.png" alt="Consultar Estado" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Consultar Estado del Campus</span>
            <span class="menu-card-subtitulo">Ver disponibilidad del campus</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Realizar reserva-->
        <router-link to="/realizar_reserva" class="menu-card" data-cy="reserva-page">
          <div class="menu-card-img">
            <img src="/reservaImagen.png" alt="Realizar Reserva" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Realizar Reserva</span>
            <span class="menu-card-subtitulo">Reserva tu bicicleta ahora</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Cancelar reserva-->
        <router-link to="/cancelar_reserva" class="menu-card" data-cy="cancelar-page">
          <div class="menu-card-img">
            <img src="/cancelarImagen.png" alt="Cancelar Reserva" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Cancelar Reserva</span>
            <span class="menu-card-subtitulo">Gestiona tus reservas activas</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Renovar contrato-->
        <router-link to="/renovar_contrato" class="menu-card" data-cy="renovar-page">
          <div class="menu-card-img">
            <img src="/renovarImagen.png" alt="Renovar Contrato" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Renovar Contrato</span>
            <span class="menu-card-subtitulo">Amplía tu periodo de uso</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
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

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(600px, 100%), 1fr));
  gap: 1.25rem;
  max-width: 1300px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.menu-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1rem 1.1rem;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  overflow: hidden;
  position: relative;
}

.menu-card::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: green;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.menu-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.09);
  border-color: #d1d5db;
  text-decoration: none;
  color: inherit;
}

.menu-card:hover::before {
  opacity: 1;
}

.menu-card-img {
  width: 30dvh;
  height: 20dvh;
  border-radius: 12px;
  background: #f0fdf4;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.menu-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.menu-card-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}

.menu-card-titulo {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  font-size: 18px;
  color: #111827;
}

.menu-card-subtitulo {
  font-size: 14px;
  color: #6b7280;
}

.menu-card-arrow {
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.2s ease, transform 0.2s ease;
}

.menu-card:hover .menu-card-arrow {
  color: green;
  transform: translateX(3px);
}

@media (max-width: 576px) {
  .menu-grid {
    grid-template-columns: 1fr;
    padding: 0 0.75rem;
  }
}
</style>
