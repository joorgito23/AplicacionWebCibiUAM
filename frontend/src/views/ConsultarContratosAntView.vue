<!-- src/views/ConsultarContratosView.vue -->
<template>
  <div id="contratos-view" style="width: 100%">
    <main>
      <h1 class="titulo-contrato" data-cy="contrato-title">
        Contratos del Sistema
      </h1>
      <div class="row justify-content-center align-items-start">
        <!-- Filtros de búsqueda -->
        <div class="col-11 col-lg-4 d-flex justify-content-center">
          <div class="card card-cibiuam">
            <h2 class="titulo text-center mb-4">🔍 Filtros de Búsqueda</h2>
            <!-- Componente de filtros -->
            <FiltrosContratos @filtrar-contratos="actualizarContratos" />
          </div>
        </div>
        <!-- Tabla de contratos -->
        <div class="col-12 col-lg-7">
          <div class="table-contenedor">
            <table class="contracts-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Tarifa</th>
                  <th>Inicio</th>
                  <th>Fin</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in contratos" :key="c.id">
                  <td>{{ c.usuario.usuario.username }}</td>
                  <td>{{ c.tarifa.duracion }}</td>
                  <td>{{ c.inicio }}</td>
                  <td>{{ c.fin }}</td>
                  <td>
                    <span v-if="new Date(c.fin) < new Date()" class="status expired">
                      Finalizado
                    </span>
                    <span v-else-if="new Date(c.inicio) > new Date()" class="status pending">
                      Pendiente de inicio
                    </span>
                    <span v-else class="status active"> Activo </span>
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
import FiltrosContratos from "../components/FiltrosContratos.vue";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "contratos-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const contratos = ref(null);

// Función que obtiene los contratos de los usuarios
const getContratos = async () => {
  try {
    // Realiza una solicitud GET para obtener los contratos del sistema
    const response = await fetch(myVar + "/cibiuam/consultar_contratos/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + authStore.token,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return;
    }

    const data = await response.json();
    contratos.value = data;
  } catch (error) {
    console.error(error);
  }
};

// Función que actualiza los contratos mostrados al gestor a partir de los filtros establecidos
const actualizarContratos = async (filtros) => {
  try {
    const datos = {};
    if (filtros.tarifa) {
      datos.tarifa = filtros.tarifa;
    }
    if (filtros.inicio) {
      datos.inicio = filtros.inicio;
    }
    if (filtros.fin) {
      datos.fin = filtros.fin;
    }
    // Realiza una solicitud POST para filtrar los contratos
    const response = await fetch(
      myVar + "/cibiuam/consultar_contratos_filtros/",
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
    contratos.value = data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getContratos();
});
</script>

<style scoped>
.titulo-contrato {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 15px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 20px auto;
}

.titulo {
  text-align: center;
  font-family: "DM Sans", sans-serif;
  font-weight: 400;
}

.table-contenedor {
  padding: 0 1rem;
  margin: 1.5rem auto;
  overflow-x: auto;
  max-height: 60dvh;
  overflow-y: auto;
  text-align: center;
}

.contracts-table {
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

.contracts-table thead {
  background: #166534;
  color: white;
}

.contracts-table th,
.contracts-table td {
  padding: 14px 16px;
  vertical-align: middle;
  white-space: normal;
  overflow-wrap: normal;
}

@media (max-width: 767px) {

  .contracts-table th,
  .contracts-table td {
    white-space: nowrap;
  }
}

.contracts-table th {
  font-weight: 600;
  letter-spacing: 0.03em;
}

.contracts-table tbody tr {
  border-bottom: 1px solid #e5e7eb;
  transition: background 0.2s ease;
}

.contracts-table tbody tr:hover {
  background: #f0fdf4;
}

.contracts-table tbody tr:last-child {
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

.status.active {
  background: #dcfce7;
  color: #166534;
}

.status.expired {
  background: #fee2e2;
  color: #991b1b;
}

.status.pending {
  background: #dbeafe;
  color: #1e3a8a;
}

@media (max-width: 576px) {

  .contracts-table th,
  .contracts-table td {
    padding: 10px 8px;
    font-size: 16px;
  }
}
</style>
