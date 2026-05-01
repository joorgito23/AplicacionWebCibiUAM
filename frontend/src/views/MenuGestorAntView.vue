<!-- src/views/MenuGestorView.vue -->
<template>
  <div id="gestor-view">
    <main>
      <!-- Acciones a realizar -->
      <h1 class="titulo-gestor">¿Qué acción desea realizar como gestor?</h1>
      <div class="row justify-content-center mb-md-5">
        <!-- Consultar estado de bicicletas y estaciones -->
        <div class="col-8 col-md-4 col-lg-2 mb-2 d-flex justify-content-center">
          <div class="card border-2 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/consultarEstado.png" alt="ConsultarEstado" class="imagen-menu img-fluid" />
            <router-link to="/consultar_estado_gestor" class="btn btn-primary mt-1 mx-auto"
              data-cy="estado-gestor-page">Consultar Estado de Bicicletas y Estaciones</router-link>
          </div>
        </div>
        <div class="d-none d-lg-block col-lg-1"></div>
        <!-- Actualizar tarifas -->
        <div class="col-8 col-md-4 col-lg-2 mb-2 d-flex justify-content-center">
          <div class="card border-2 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/tarifasMenu.png" alt="tarifas" class="imagen-menu img-fluid" />
            <router-link to="/actualizar_tarifas" class="btn btn-primary mt-auto mx-auto"
              data-cy="act-tar-page">Actualizar Tarifas</router-link>
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Alta de estación -->
        <div class="col-8 col-md-4 col-lg-2 mb-2 d-flex justify-content-center">
          <div class="card border-2 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/altaEstMenu.png" alt="altaEstacion" class="imagen-menu img-fluid" />
            <router-link to="/alta_estacion" class="btn btn-primary mt-1 mx-auto" data-cy="est-page">Alta de
              Estación</router-link>
          </div>
        </div>
        <div class="d-none d-lg-block col-lg-1"></div>
        <!-- Alta de bicicleta -->
        <div class="col-8 col-md-4 col-lg-2 mb-2 d-flex justify-content-center">
          <div class="card border-2 rounded-4 p-2 h-100 d-flex flex-column">
            <img src="/altaBiciMenu.png" alt="altaBici" class="imagen-menu img-fluid" />
            <router-link to="/alta_bicicleta" class="btn btn-primary mt-1 mx-auto" data-cy="bici-page">Alta de
              Bicicleta</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: "gestor-view" });
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
</style>
