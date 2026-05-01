<!-- src/views/MenuAdminView.vue -->
<template>
  <div id="admin-view" style="width: 100%">
    <main>
      <h1 class="titulo-admin">
        ¿Qué acción desea realizar como administrador?
      </h1>
      <div class="row justify-content-center mt-3">
        <div class="col-10 col-lg-5 justify-content-center">
          <div class="card card-cibiuam">
            <h2 class="titulo" data-cy="alta-tit">
              <img src="/agregar-usuario.png" alt="Alta" class="icono-titulo" />
              Alta de Gestor
            </h2>
            <!-- Formulario de alta -->
            <FormularioAltaGestor @altaGestor="crearGestor" :borrarFormulario="borrarFormulario" />
            <div class="contenedor">
              <div v-if="mensaje">
                <p class="alert alert-success" data-cy="msg">{{ mensaje }}</p>
              </div>
              <div v-if="mensajeError">
                <p class="alert alert-danger">{{ mensajeError }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Tabla de gestores para dar de baja -->
        <div class="col-10 col-lg-5">
          <div class="card card-cibiuam w-100">
            <h2 class="titulo" data-cy="alta-tit">
              <img src="/usuario.png" alt="Baja" class="icono-titulo" /> Baja de
              Gestor
            </h2>
            <div class="table-contenedor">
              <table class="gestor-table">
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Nombre</th>
                    <th>Apellidos</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="g in gestores" :key="g.usuario.username">
                    <td>{{ g.usuario.username }}</td>
                    <td>{{ g.nombre }}</td>
                    <td>{{ g.apellidos }}</td>
                    <td>
                      <button class="status cancelada" @click="abrirModal(g.usuario.username)"
                        :data-cy="'boton-' + g.usuario.username">
                        Eliminar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="contenedor">
              <div v-if="mensajeBaja">
                <p class="alert alert-success" data-cy="msgBaja">
                  {{ mensajeBaja }}
                </p>
              </div>
              <div v-if="mensajeBajaError">
                <p class="alert alert-danger">{{ mensajeBajaError }}</p>
              </div>
            </div>

            <div v-if="mostrarModal" class="modal-overlay" @click.self="mostrarModal = false">
              <div class="modal-confirmacion">
                <h4>¿Eliminar gestor {{ gestorEliminar }}?</h4>
                <p>Esta acción no se puede deshacer.</p>
                <div class="modal-actions">
                  <button class="btn-secundario" @click="mostrarModal = false">
                    Volver
                  </button>
                  <button class="btn-cancelar" @click="eliminarGestor" data-cy="confirmarBaja">
                    Sí, eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FormularioAltaGestor from "../components/FormularioAltaGestor.vue";
import { useAuthStore } from "@/stores/auth";
import { ref, onMounted } from "vue";
defineOptions({ name: "admin-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();

const mensaje = ref("");
const mensajeError = ref("");
const mensajeBaja = ref("");
const mensajeBajaError = ref("");
const borrarFormulario = ref(false);

// Función para crear un nuevo gestor en el sistema
const crearGestor = async (persona) => {
  try {
    // Realiza una solicitud POST a la API para crear el gestor
    const response = await fetch(myVar + "/cibiuam/alta_gestor/", {
      method: "POST",
      body: JSON.stringify(persona),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeError.value = "";
      }, 3000);
      return;
    }

    const data = await response.json();
    mensaje.value = data.Mensaje;
    setTimeout(() => {
      mensaje.value = "";
    }, 3000);

    // Actualiza la lista de gestores para mostrar los datos actualizados
    getGestores();

    // Limpia el formulario
    borrarFormulario.value = true;
    setTimeout(() => (borrarFormulario.value = false), 0);
  } catch (error) {
    console.error(error);
  }
};

const gestores = ref([]);

// Función que obtiene los gestores del sistema
const getGestores = async () => {
  try {
    // Realiza una solicitud GET para obtener los gestores
    const response = await fetch(myVar + "/cibiuam/informacion/gestores/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = "Error al obtener informacion de las gestores";
      return;
    }

    const data = await response.json();
    gestores.value = data;
  } catch (error) {
    console.error(error);
  }
};

const mostrarModal = ref(false);
const gestorEliminar = ref(null);

// Función para abrir la confirmación
const abrirModal = (username) => {
  gestorEliminar.value = username;
  mostrarModal.value = true;
};

// Función que elimina un gestor del sistema
const eliminarGestor = async () => {
  try {
    // Realiza una solicitud DELETE para eliminar el gestor seleccionado
    const response1 = await fetch(myVar + "/cibiuam/baja_gestor/", {
      method: "DELETE",
      body: JSON.stringify({ usuario: gestorEliminar.value }),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response1.ok) {
      const errorData = await response1.json();
      console.error("Error:", errorData);
      mensajeBajaError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeBajaError.value = "";
      }, 3000);
      mostrarModal.value = false;
      gestorEliminar.value = null;
      return;
    }

    const data1 = await response1.json();
    mensajeBaja.value = data1.Mensaje;

    // Actualiza la tabla de gestores
    getGestores();
    setTimeout(() => {
      mensajeBaja.value = "";
    }, 3000);
    mostrarModal.value = false;
    gestorEliminar.value = null;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getGestores();
});
</script>

<style scoped>
.titulo-admin {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  margin: 20px auto;
  overflow: visible;
}

.titulo {
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 1rem;
}

.table-contenedor {
  overflow-x: auto;
  text-align: center;
  max-height: 50dvh;
  overflow-y: auto;
}

.gestor-table {
  display: table;
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
  background: rgb(238, 238, 238);
  border-radius: 12px;
  overflow: hidden;
  font-family: "Playfair Display", serif;
  font-size: 18px;
  text-align: center;
  table-layout: auto;
}

.gestor-table thead {
  background: #166534;
  color: white;
}

.gestor-table th,
.gestor-table td {
  padding: 14px 16px;
  vertical-align: middle;
  white-space: normal;
  overflow-wrap: normal;
}

@media (max-width: 767px) {

  .gestor-table th,
  .gestor-table td {
    white-space: nowrap;
  }
}

.gestor-table th {
  font-weight: 600;
  letter-spacing: 0.03em;
}

.gestor-table tbody tr {
  border-bottom: 1px solid #e5e7eb;
  transition: background 0.2s ease;
}

.gestor-table tbody tr:hover {
  background: #f0fdf4;
}

.gestor-table tbody tr:last-child {
  border-bottom: none;
}

.status {
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 999px;
  display: inline-block;
  font-size: 0.85rem;
  text-align: center;
}

.status.cancelada {
  background: #fee2e2;
  color: #991b1b;
}

.icono-titulo {
  width: 35px;
  height: 35px;
  vertical-align: middle;
  margin-right: 0.25rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-confirmacion {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 380px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  z-index: 10000;
  position: relative;
}

.modal-confirmacion h4 {
  margin: 0 0 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-secundario {
  padding: 0.5rem 1.25rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

.btn-cancelar {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  justify-content: center;
  padding: 8px 16px;
  border: 1.5px solid #fca5a5;
  background: #fff5f5;
  color: #dc2626;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
}

.btn-cancelar:hover {
  background: #fee2e2;
  border-color: #dc2626;
}
</style>
