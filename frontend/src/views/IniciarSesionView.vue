<!-- src/views/IniciarSesionView.vue-->
<template>
  <div id="login-view">
    <main>
      <div class="card card-cibiuam">
        <h1 class="titulo-login">Inicio de Sesión CibiUAM</h1>
        <div>
          <!-- Formulario de login -->
          <formulario-login @login="loginUsuario" />
          <div class="contenedor">
            <div v-if="mensajeError" class="alert alert-danger msg-error" data-cy="error">
              {{ mensajeError }}
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-column justify-content-center align-items-center">
        <!-- Acceso directo para registrarse -->
        <div class="card card-cibiuam">
          <h3 class="titulo-tarjeta">¿Aún no viajas en CibiUAM?</h3>
          <div class="enlace-registro">
            <span><router-link to="/alta_usuario">Registrarse</router-link></span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FormularioLogin from "@/components/FormularioLogin.vue";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
defineOptions({ name: "home-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const mensajeError = ref("");
const authStore = useAuthStore();
const router = useRouter();

// Función para realizar el login
const loginUsuario = async (persona) => {
  try {
    // Realiza una solicitud POST para intentar autenticar al usuario
    const response = await fetch(myVar + "/auth/token/login/", {
      method: "POST",
      body: JSON.stringify(persona),
      headers: { "Content-type": "application/json; charset=UTF-8" },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = "Error: credenciales incorrectas";
      setTimeout(() => {
        mensajeError.value = "";
      }, 4000);
      return;
    }

    // Si la autenticación fue exitosa, guardamos el token de autenticación
    const data = await response.json();
    authStore.setToken(data.auth_token, persona.username, data.rol);

    // Redirigimos al usuario a su pantalla correspondiente en función de su rol
    if (data.rol == "usuario") {
      router.push("/menu_usuario");
    } else if (data.rol == "gestor") {
      router.push("/menu_gestor");
    } else {
      router.push("/menu_admin");
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 30px 20px;
}

.titulo-login {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 2rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 0.25rem;
  margin-right: 0.25rem;
}

.msg-error {
  margin-top: 1rem;
  font-size: 18px;
}

.titulo-tarjeta {
  margin-bottom: 16px;
  color: black;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.enlace-registro {
  display: flex;
  flex-direction: column;
  font-size: 19px;
}

.enlace-registro span {
  background: #eaf4e8;
  border-radius: 6px;
  padding: 10px 1px;
  line-height: 1.8;
  border: 2px solid black;
}
</style>
