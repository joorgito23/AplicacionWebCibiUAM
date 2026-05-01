<!-- src/views/MenuGestorView.vue -->
<template>
  <div id="gestor-view">
    <main>
      <h1 class="titulo-gestor">¡Bienvenido, {{ usuario }}!</h1>
      <!-- Acciones del gestor-->
      <div class="menu-grid">
        <!-- Consultar estado-->
        <router-link to="/consultar_estado_gestor" class="menu-card" data-cy="estado-gestor-page">
          <div class="menu-card-img">
            <img src="/estadoGestor.png" alt="Consultar Estado" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Consultar Estado de Bicicletas y Estaciones</span>
            <span class="menu-card-subtitulo">Ver disponibilidad del campus</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Actualizar tarifas-->
        <router-link to="/actualizar_tarifas" class="menu-card" data-cy="act-tar-page">
          <div class="menu-card-img">
            <img src="/tarifaGestor.png" alt="Act tarifa" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Actualizar Tarifas</span>
            <span class="menu-card-subtitulo">Modifica el importe y precio por minuto de una tarifa</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Alta de estación-->
        <router-link to="/alta_estacion" class="menu-card" data-cy="est-page">
          <div class="menu-card-img">
            <img src="/estGestor.png" alt="Estacion" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Alta de Estación</span>
            <span class="menu-card-subtitulo">Crea una nueva estación en el campus de la UAM</span>
          </div>
          <div class="menu-card-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
        <!-- Alta de bicicleta-->
        <router-link to="/alta_bicicleta" class="menu-card" data-cy="bici-page">
          <div class="menu-card-img">
            <img src="/biciGestor.png" alt="Bici" class="img-fluid" />
          </div>
          <div class="menu-card-body">
            <span class="menu-card-titulo">Alta de Bicicleta</span>
            <span class="menu-card-subtitulo">Registra una nueva bicicleta en una estación del campus de la
              UAM</span>
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
defineOptions({ name: "gestor-view" });
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();
const usuario = authStore.usuario;
</script>

<style scoped>
.titulo-gestor {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.imagen-menu {
  border-radius: 15px;
}

.btn-primary {
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
  width: 100%;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
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
