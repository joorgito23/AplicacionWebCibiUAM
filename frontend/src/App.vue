<!-- App.vue -->
<template>
  <div class="app-background">
    <!-- Header común -->
    <header class="app-header">
      <div class="container-fluid position-relative">
        <div class="d-flex align-items-center justify-content-between py-2">
          <!-- Logo UAM en la izquierda -->
          <div class="d-flex align-items-center">
            <a href="https://www.uam.es/uam/inicio"><img src="/uam.png" alt="Logo CibiUAM"
                class="uam-movil d-block d-md-none" /></a>
            <a href="https://www.uam.es/uam/inicio"><img src="/marcaUAM_AhorizontalColor.png" alt="Logo CibiUAM"
                class="uam-md d-none d-md-block" /></a>
          </div>
          <!-- Título CibiUAM en el centro -->
          <h1 class="titulo position-absolute top-50 start-50 translate-middle m-0" @click="inicio"
            style="cursor: pointer">
            CibiUAM
          </h1>
          <!-- Enlaces de navegación en la derecha -->
          <!-- En pantallas grandes, se muestran todos los enlaces -->
          <div class="d-none d-lg-flex align-items-center enlaces">
            <span v-for="(link, i) in headerLinks || [{ to: '/', text: 'Inicio' }]" :key="i" class="nav-link"
              :class="{ active: route.path === link.to }" style="cursor: pointer" @click="
                link.action === 'logout' ? logout() : router.push(link.to)
                " :data-cy="link.to">
              <template v-if="link.to === '/consultar_perfil'">
                <img src="/avatar.png" alt="Avatar" style="width: 22px; height: 22px; margin-right: 0.25rem" />
              </template>
              {{ getLinkText(link) }}
            </span>
          </div>
          <!-- En pantallas medianas y pequeñas, se muestra un desplegable -->
          <div class="dropdown d-lg-none">
            <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
              Más
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li v-for="(link, i) in headerLinks || [
                { to: '/', text: 'Inicio' },
              ]" :key="i">
                <span class="dropdown-item" style="cursor: pointer"
                  @click="link.action ? logout() : $router.push(link.to)">
                  <template v-if="link.to === '/consultar_perfil'">
                    <img src="/avatar.png" alt="Avatar" style="width: 22px; height: 22px; margin-right: 0.25rem" />
                  </template>
                  {{ getLinkText(link) }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </header>
    <!-- Main y footer -->
    <main class="app-container">
      <div :class="['contenido', fondoVista]">
        <router-view />
      </div>
      <footer class="app-footer">© 2026 Copyright J.Pedraza Ortega</footer>
    </main>
  </div>
</template>

<style scoped>
.app-background {
  min-height: 100dvh;
  display: flex;
  background-color: white;
  flex-direction: column;
}

.app-header {
  background-color: white;
}

.uam-movil {
  border-radius: 15px;
  width: clamp(48px, 3.5vw, 120px);
  height: auto;
  margin: 0.05rem;
}

.uam-md {
  width: clamp(120px, 12.5vw, 250px);
  height: auto;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.titulo {
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
  text-align: center;
  letter-spacing: 1px;
  color: #4a7729;
  font-style: italic;
}

.enlaces {
  gap: 1.5rem;
  margin-right: 1rem;
}

.nav-link:hover {
  color: green;
}

.nav-link {
  font-weight: bold;
}

.nav-link.active {
  border-bottom: 2px solid green;
}

.app-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #75f17f47;
}

.contenido {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.contenido-foto {
  background-image: linear-gradient(rgba(255, 255, 255, 0.7),
      rgba(255, 255, 255, 0.7)),
    url("/plaza.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100%;
}

.app-footer {
  text-align: center;
  font-size: 0.9rem;
  color: black;
  padding: 10px 0;
  font-weight: bold;
  background-color: white;
}
</style>

<script setup>
import { RouterView } from "vue-router";
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "App" });

const myVar = import.meta.env.VITE_DJANGOURL;
const route = useRoute();
const authStore = useAuthStore();
const router = useRouter();

// Función que obtiene los enlaces que aparecerán en la navegación del header en función de la ruta actual
const headerLinks = computed(() => {
  if (route.meta.headerLinks) {
    return route.meta.headerLinks;
  }
  if (authStore.token !== null && authStore.token !== "") {
    return route.meta.headerLinksLogin || [{ to: "/", text: "Inicio" }];
  } else {
    return route.meta.headerLinksLogout || [{ to: "/", text: "Inicio" }];
  }
});

// Determina si se va a usar la foto de la plaza mayor de la UAM como fondo o no en función de la ruta
const fondoVista = computed(() => {
  return route.name === "login" ||
    route.name === "alta_usuario" ||
    route.name === "renovar_contrato" ||
    route.name === "menu_admin" ||
    route.name === "home"
    ? "contenido-foto"
    : "contenido";
});

// Función para obtener el nombre del usuario
const getLinkText = (link) => {
  if (link.to === "/consultar_perfil") {
    return authStore.usuario ? `${authStore.usuario}` : "Mi Perfil";
  }
  return link.text;
};

// Función que realiza el logout de la aplicación comunicándose con la API de Django
const logout = async () => {
  try {
    // Realiza una solicitud POST para cerrar sesión
    await fetch(myVar + "/auth/token/logout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    // Limpia el token
    authStore.clearToken();

    // Redirige a la pantalla inicial
    router.push("/");
  } catch (error) {
    console.error(error);
  }
};

// Vuelve al menú inicial tras pulsar el título CibiUAM
const inicio = () => {
  let headerLinks = [];

  if (route.meta.headerLinks) {
    headerLinks = route.meta.headerLinks;
  } else if (authStore.token !== null && authStore.token !== "") {
    headerLinks = route.meta.headerLinksLogin || [];
  } else {
    headerLinks = route.meta.headerLinksLogout || [];
  }
  const inicio = headerLinks.find((link) => link.text === "Inicio");

  if (inicio) {
    router.push(inicio.to);
  }
};
</script>
