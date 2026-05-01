<!-- src/componets/FormularioAltaGestor.vue -->
<template>
  <div id="formulario-alta-gestor">
    <form @submit.prevent="altaGestor">
      <div class="row justify-content-center">
        <!-- Nombre -->
        <div class="col-md-6 col-10 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Nombre:</label>
          <input v-model="persona.nombre" type="text" class="form-control" placeholder="Escriba aquí..."
            data-cy="nombre" />
        </div>
        <!-- Apellidos -->
        <div class="col-md-6 col-10 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Apellidos:</label>
          <input v-model="persona.apellidos" type="text" class="form-control" placeholder="Escriba aquí..."
            data-cy="apellidos" />
        </div>
      </div>
      <div class="row justify-content-center align-items-start">
        <!-- Usuario -->
        <div class="col-md-6 col-10 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Usuario:</label>
          <input v-model="persona.usuario" type="text" class="form-control" placeholder="Escriba aquí..."
            data-cy="usuario" />
          <div class="req-list mt-1">
            <span class="req" :class="persona.usuario.length >= 4 ? 'ok' : 'fail'">
              <span class="req-icon">{{
                persona.usuario.length >= 4 ? "✓" : "✗"
                }}</span>
              Mínimo 4 caracteres
            </span>
          </div>
        </div>
        <!-- Contraseña -->
        <div class="col-md-6 col-10 d-flex flex-column justify-content-center mb-3">
          <label class="align-self-start"><span class="text-danger">*</span> Contraseña:</label>
          <div class="contenedor-password">
            <input v-model="persona.contraseña" :type="mostrarPassword ? 'text' : 'password'" class="form-control"
              placeholder="Escriba aquí..." data-cy="contraseña" />
            <img :src="mostrarPassword ? '/invisible.png' : '/ojo.png'" class="visible"
              @click="mostrarPassword = !mostrarPassword" alt="Mostrar / Ocultar contraseña" />
          </div>
          <div class="req-list mt-1">
            <span class="req" :class="persona.contraseña.length >= 8 ? 'ok' : 'fail'">
              <span class="req-icon">{{
                persona.contraseña.length >= 8 ? "✓" : "✗"
                }}</span>
              Mínimo 8 caracteres
            </span>
            <span class="req" :class="/[A-Z]/.test(persona.contraseña) ? 'ok' : 'fail'">
              <span class="req-icon">{{
                /[A-Z]/.test(persona.contraseña) ? "✓" : "✗"
                }}</span>
              Al menos 1 mayúscula
            </span>
            <span class="req" :class="/[0-9]/.test(persona.contraseña) ? 'ok' : 'fail'">
              <span class="req-icon">{{
                /[0-9]/.test(persona.contraseña) ? "✓" : "✗"
                }}</span>
              Al menos 1 número
            </span>
            <span class="req" :class="/[^a-zA-Z0-9]/.test(persona.contraseña) ? 'ok' : 'fail'">
              <span class="req-icon">{{
                /[^a-zA-Z0-9]/.test(persona.contraseña) ? "✓" : "✗"
                }}</span>
              Al menos 1 símbolo (!@#$...)
            </span>
          </div>
        </div>
      </div>
      <!-- Botón de alta -->
      <div class="row justify-content-center">
        <div class="col-auto">
          <div class="form-group">
            <button class="btn btn-primary" data-cy="alta-gest">
              Alta Gestor
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

defineOptions({
  name: "formulario-alta-gestor",
});

const props = defineProps({
  borrarFormulario: Boolean,
});

const persona = ref({
  nombre: "",
  apellidos: "",
  usuario: "",
  contraseña: "",
});

const emit = defineEmits(["altaGestor"]);

// Función para enviar los datos del nuevo gestor a la vista correspondiente
const altaGestor = () => {
  emit("altaGestor", persona.value);
};

// Monitoriza el envío del formulario para dejar el formulario en blanco de nuevo
watch(
  () => props.borrarFormulario,
  (flag) => {
    if (flag) {
      persona.value.nombre = "";
      persona.value.apellidos = "";
      persona.value.usuario = "";
      persona.value.contraseña = "";
    }
  }
);

// Variable para mostrar o no la contraseña
const mostrarPassword = ref(false);
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

.req-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 5px;
}

.req {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6c757d;
  transition: color 0.2s;
}

.req.ok {
  color: #198754;
}

.req.fail {
  color: #dc3545;
}

.req-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  flex-shrink: 0;
  background-color: #6c757d;
  color: #fff;
  transition: background-color 0.2s;
}

.req.ok .req-icon {
  background-color: #198754;
}

.req.fail .req-icon {
  background-color: #dc3545;
}
</style>
