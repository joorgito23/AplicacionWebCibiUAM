<!-- src/views/CancelarReservaView.vue -->
<template>
  <div id="cancelar-view" style="width: 100%">
    <main>
      <h1 class="titulo-cancelar" data-cy="cancelar-title">
        Cancelación de Reservas
      </h1>
      <div class="row justify-content-center mt-3">
        <div class="col-11 col-md-8 d-flex justify-content-center mb-1">
          <p class="instrucciones">
            A continuación podrá consultar todas las reservas pendientes de
            realización para su cancelación. Para ello, deberá marcar la opción
            de cancelar en la reserva que desee cancelar.
          </p>
        </div>
      </div>
      <!-- Tabla de reservas disponibles para cancelar -->
      <div class="row justify-content-center mt-1">
        <div class="col-12 col-md-8">
          <div class="table-contenedor">
            <table class="reservas-table">
              <thead>
                <tr>
                  <th>Id</th>
                  <th>Origen</th>
                  <th>Destino</th>
                  <th>Inicio</th>
                  <th>Fin</th>
                  <th>Estado</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in reservas" :key="r.id">
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    {{ r.id }}
                  </td>
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    {{ r.estOrigen.nombre }}, nº{{ r.ancOrigen.numAnclaje }}
                  </td>
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    {{ r.estDestino.nombre }}, nº{{ r.ancDestino.numAnclaje }}
                  </td>
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    {{ r.fechaInicio }}
                  </td>
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    {{ r.fechaFin }}
                  </td>
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
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
                  <td v-if="
                    new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
                    r.estado !== 'cancelada'
                  ">
                    <button class="status cancelada" @click="cancelar(r.id)" :data-cy="'boton-' + r.id">
                      Cancelar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="contenedor">
        <div v-if="mensaje">
          <p class="alert alert-success" data-cy="msg">{{ mensaje }}</p>
        </div>
        <div v-if="mensajeError">
          <p class="alert alert-danger">{{ mensajeError }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: "cancelar-view" });
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const reservas = ref([]);

// Función que obtiene las reservas pendientes del usuario
const getReservas = async () => {
  try {
    const datos = {};
    datos.inicio = new Date().toISOString().split("T")[0];

    // Realiza una solicitud POST para obtener las reservas pendientes del usuario
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
      return;
    }

    const data = await response.json();
    // Guarda las reservas para mostrar al usuario mediante una tabla
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

const mensajeError = ref("");
const mensaje = ref("");

// Función que cancela una reserva del usuario
const cancelar = async (id) => {
  try {
    // Realiza una solicitud POST para cancelar la reserva
    const datos = {
      reserva_id: id,
    };
    const response = await fetch(myVar + "/cibiuam/cancelar_reserva/", {
      method: "POST",
      body: JSON.stringify(datos),
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

    // Obtiene las reservas actualizadas tras la cancelación
    getReservas();
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getReservas();
});
</script>

<style scoped>
.titulo-cancelar {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin: 0 auto 1rem auto;
  padding: 0 1rem;
}

.table-contenedor {
  padding: 0 1rem;
  margin: 1rem auto;
  overflow-x: auto;
  text-align: center;
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

@media (max-width: 576px) {

  .reservas-table th,
  .reservas-table td {
    padding: 10px 8px;
    font-size: 15px;
  }
}

.status {
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 999px;
  display: inline-block;
  font-size: 0.85rem;
  text-align: center;
}

.status.finalizada {
  background: #e5e7eb;
  color: #374151;
}

.status.cancelada {
  background: #fee2e2;
  color: #991b1b;
}

.status.encurso {
  background: #dcfce7;
  color: #166534;
}

.status.pendiente {
  background: #fef9c3;
  color: #1e3a8a;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 2rem;
  margin-right: 2rem;
}
</style>
