<!-- src/components/FormularioLogin.vue -->
<template>
  <div id="formulario-login">
    <form @submit.prevent="enviarCredenciales">
      <div>
        <!-- Usuario -->
        <div class="row mb-2 justify-content-center">
          <div class="col-10 col-md-8 d-flex flex-column justify-content-center">
            <label for="username" class="align-self-start">Usuario:</label>
            <input v-model="persona.username" type="text" id="username" class="form-control mb-3"
              placeholder="Introduzca usuario" data-cy="username" />
          </div>
        </div>
        <!-- Contraseña -->
        <div class="row mb-4 justify-content-center">
          <div class="col-10 col-md-8 d-flex flex-column">
            <label for="password" class="align-self-start">Contraseña:</label>
            <div class="contenedor-password">
              <input v-model="persona.password" :type="mostrarPassword ? 'text' : 'password'" id="password"
                class="form-control" placeholder="Introduzca contraseña" data-cy="password" />
              <img :src="mostrarPassword ? '/invisible.png' : '/ojo.png'" class="visible"
                @click="mostrarPassword = !mostrarPassword" alt="Mostrar / Ocultar contraseña" />
            </div>
          </div>
        </div>
        <!-- Botón de login -->
        <div class="row justify-content-center">
          <div class="col-auto">
            <button class="btn btn-primary" data-cy="login-button">
              Iniciar Sesión
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
<script setup>
import { ref } from "vue";
defineOptions({
  name: "formulario-login",
});

// Variable para mostrar o no la contraseña
const mostrarPassword = ref(false);

// Variable para enviar las credenciales del usuario registradas en el formulario
const persona = ref({
  username: "",
  password: "",
});

const emit = defineEmits(["login"]);

// Función que envía los datos introducidos por el usuario a la vista para verificar el acceso
const enviarCredenciales = () => {
  emit("login", persona.value);
};
</script>

<style scoped>
.btn-primary {
  margin: 10px;
  font-size: 18px;
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
