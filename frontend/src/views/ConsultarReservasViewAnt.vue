<!-- src/views/ConsultarReservasView.vue -->
<template>
  <div id="reservas-view" style="width: 100%">
    <main>
      <h1 class="titulo-reservas" data-cy="reservas-title">
        Reservas del Usuario
      </h1>
      <!-- Filtros de reservas -->
      <FiltrosReservas @filtrar-reservas="actualizarReservas" />
      <div class="contenedor">
        <div v-if="mensajeError">
          <p class="alert alert-danger">{{ mensajeError }}</p>
        </div>
      </div>
      <!-- Tabla con las reservas del usuario -->
      <div class="row justify-content-center mt-4">
        <div class="col-12 col-lg-8">
          <div class="table-contenedor">
            <table class="reservas-table">
              <thead>
                <tr>
                  <th>Origen</th>
                  <th>Destino</th>
                  <th>Inicio</th>
                  <th>Fin</th>
                  <th>Código</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in reservas" :key="r.id">
                  <td>
                    {{ r.estOrigen.nombre }}, nº{{ r.ancOrigen.numAnclaje }}
                  </td>
                  <td>
                    {{ r.estDestino.nombre }}, nº{{ r.ancDestino.numAnclaje }}
                  </td>
                  <td>{{ r.fechaInicio }}</td>
                  <td>{{ r.fechaFin }}</td>
                  <td>{{ r.codigoRecogida }}</td>
                  <td>
                    <span v-if="r.estado === 'cancelada'" class="status cancelada">
                      Cancelada
                    </span>
                    <span v-else-if="
                      new Date(r.fechaFin.replace(' ', 'T')) < new Date()
                    " class="status finalizada">
                      Finalizada
                    </span>
                    <span v-else-if="
                      new Date(r.fechaInicio.replace(' ', 'T')) <
                      new Date() &&
                      new Date(r.fechaFin.replace(' ', 'T')) > new Date()
                    " class="status encurso">
                      En curso
                    </span>
                    <span v-else class="status pendiente">
                      Pendiente de inicio
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FiltrosReservas from "../components/FiltrosReservas.vue";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "reservas-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const mensajeError = ref("");
const reservas = ref(null);

// Función que obtiene las reservas del usuario
const getReservas = async () => {
  try {
    // Realiza una solicitud GET a la API para obtener las reservas del usuario
    const response = await fetch(myVar + "/cibiuam/consultar_reservas/", {
      method: "GET",
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
      }, 4000);
      return;
    }

    // Guarda las reservas del usuario para mostrarlas por pantalla
    const data = await response.json();
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

// Función que filtra las reservas mostradas a partir de los filtros introducidos por el usuario
const actualizarReservas = async (filtros) => {
  try {
    const datos = {};
    if (filtros.origen) {
      datos.origen = filtros.origen;
    }
    if (filtros.inicio) {
      datos.inicio = filtros.inicio;
    }
    if (filtros.fin) {
      datos.fin = filtros.fin;
    }
    if (filtros.destino) {
      datos.destino = filtros.destino;
    }
    // Realiza una solicitud  POST para obtener las reservas filtradas
    const response = await fetch(
      myVar + "/cibiuam/consultar_reservas_filtros/",
      {
        method: "POST",
        body: JSON.stringify(datos),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + authStore.token,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      mensajeError.value = errorData.Mensaje;
      setTimeout(() => {
        mensajeError.value = "";
      }, 4000);
      return;
    }

    // Actualiza las reservas a mostrar
    const data = await response.json();
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getReservas();
});
</script>

<style scoped>
.titulo-reservas {
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 2rem;
  margin-right: 2rem;
}

.table-contenedor {
  padding: 0 1rem;
  margin: 1.5rem auto;
  overflow-x: auto;
  text-align: center;
  max-height: 80dvh;
  overflow-y: auto;
}

.reservas-table {
  display: table;
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  font-family: "Playfair Display", serif;
  font-size: 18px;
  text-align: center;
  table-layout: auto;
}

.reservas-table thead {
  background: #166534;
  color: white;
}

.reservas-table th,
.reservas-table td {
  padding: 14px 16px;
  vertical-align: middle;
  white-space: normal;
  overflow-wrap: normal;
}

@media (max-width: 767px) {

  .reservas-table th,
  .reservas-table td {
    white-space: nowrap;
  }
}

.reservas-table th {
  font-weight: 600;
  letter-spacing: 0.03em;
}

.reservas-table tbody tr {
  border-bottom: 1px solid #e5e7eb;
  transition: background 0.2s ease;
}

.reservas-table tbody tr:hover {
  background: #f0fdf4;
}

.reservas-table tbody tr:last-child {
  border-bottom: none;
}

.status {
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 100px;
  display: inline-block;
  font-size: 0.85rem;
  text-align: center;
}

.status.encurso {
  background: #dcfce7;
  color: #166534;
}

.status.cancelada {
  background: #fee2e2;
  color: #991b1b;
}

.status.pendiente {
  background: #dbeafe;
  color: #1e3a8a;
}

.status.finalizada {
  background: #e5e7eb;
  color: #374151;
}

@media (max-width: 576px) {

  .reservas-table th,
  .reservas-table td {
    padding: 10px 8px;
    font-size: 16px;
  }
}
</style>
