<!-- src/components/FormularioAlta.vue -->
<template>
  <div id="formulario-alta-usuario">
    <form @submit.prevent="altaUsuario">
      <div class="row justify-content-center">
        <!-- Nombre -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Nombre:</label>
          <input v-model="persona.nombre" type="text" class="form-control" placeholder="Escribe aquí..."
            data-cy="nombre" />
        </div>
        <!-- Apellidos -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Apellidos:</label>
          <input v-model="persona.apellidos" type="text" class="form-control" placeholder="Escribe aquí..."
            data-cy="apellidos" />
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Usuario -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Usuario:</label>
          <input v-model="persona.usuario" type="text" class="form-control" placeholder="Escribe aquí..."
            data-cy="usuario" usuario />
        </div>
        <!-- Contraseña -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Contraseña:</label>
          <div class="contenedor-password">
            <input v-model="persona.contraseña" :type="mostrarPassword ? 'text' : 'password'" class="form-control"
              placeholder="Escribe aquí..." data-cy="contraseña" />
            <img :src="mostrarPassword ? '/invisible.png' : '/ojo.png'" class="visible"
              @click="mostrarPassword = !mostrarPassword" alt="Mostrar / Ocultar contraseña" />
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <!-- Teléfono -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Teléfono:</label>
          <input v-model="persona.tlf" type="text" class="form-control" placeholder="Escribe aquí..." data-cy="tlf" />
        </div>
        <!-- Tarifa -->
        <div class="col-lg-5 col-11 d-flex flex-column justify-content-center mb-3">
          <SelectorTarifaAlta @enviar-tarifa="actualizar" labelClass="text-start" />
        </div>
      </div>
      <!-- Botón de alta -->
      <div class="row justify-content-center">
        <div class="col-auto">
          <button class="btn btn-primary" data-cy="alta-button">
            Alta Usuario
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import SelectorTarifaAlta from "./SelectorTarifaAlta.vue";

defineOptions({
  name: "formulario-alta-usuario",
});

// Datos introducidos por el usuario en el formulario
const persona = ref({
  nombre: "",
  apellidos: "",
  usuario: "",
  contraseña: "",
  tlf: "",
  tarifa: "",
});

// Variable para mostrar o no la contraseña
const mostrarPassword = ref(false);

// Función para guardar la tarifa deseada por el usuario
const actualizar = (tarifa) => {
  persona.value.tarifa = tarifa;
};

const emit = defineEmits(["alta"]);
// Función para enviar los datos del formulario a la vista correspondiente para realizar el alta de usuario
const altaUsuario = () => {
  emit("alta", persona.value);
};
</script>

<style scoped>
.btn-primary {
  margin: 10px;
  font-size: 17px;
  background-color: green !important;
  border-color: black !important;
}

.btn-primary:hover {
  background-color: #0077c8 !important;
}

.contenedor-password {
  position: relative;
}

.contenedor-password input {
  padding-right: 40px;
}

.visible {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  width: 20px;
  height: 20px;
  object-fit: contain;
}
</style>
