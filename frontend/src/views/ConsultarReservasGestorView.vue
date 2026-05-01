<!-- src/views/ConsultarReservasGestorView.vue -->
<template>
  <div id="reservas-gestor-view" style="width: 100%">
    <main>
      <h1 class="titulo-reservas-gestor" data-cy="reservas-gestor-title">
        Historial de Reservas
      </h1>
      <!-- Filtros de las reservas -->
      <FiltrosReservasGestor @filtrar-reservas-gestor="actualizarReservas" />
      <div class="contenedor">
        <div v-if="mensajeError">
          <p class="alert alert-danger">{{ mensajeError }}</p>
        </div>
      </div>
      <!-- Tarjetas de reservas del sistema -->
      <div class="reservas-grid">
        <div v-for="r in reservas" :key="r.id" class="reserva-card" :class="getEstadoClass(r)">
          <div class="card-borde"></div>
          <div class="card-header">
            <div class="ruta">
              <div class="lugar">
                <span class="lugar-nombre">{{ r.estOrigen.nombre }}</span>
                <span class="lugar-anclaje">Anclaje nº{{ r.ancOrigen.numAnclaje }}</span>
              </div>
              <div class="ruta-flecha">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
              <div class="lugar lugar-destino">
                <span class="lugar-nombre">{{ r.estDestino.nombre }}</span>
                <span class="lugar-anclaje">Anclaje nº{{ r.ancDestino.numAnclaje }}</span>
              </div>
            </div>
            <span :class="['etiqueta-estado', getEstadoClass(r)]">
              {{ getEstadoLabel(r) }}
            </span>
          </div>
          <div class="card-body">
            <div class="info-item">
              <span class="info-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </span>
              <span class="info-label">Usuario</span>
              <span class="info-value">{{ r.usuario.usuario.username }}</span>
            </div>
            <div class="info-item">
              <span class="info-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
              </span>
              <span class="info-label">Inicio</span>
              <span class="info-value">{{ formatFecha(r.fechaInicio) }}</span>
            </div>
            <div class="info-item">
              <span class="info-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
              </span>
              <span class="info-label">Fin</span>
              <span class="info-value">{{ formatFecha(r.fechaFin) }}</span>
            </div>
            <div class="info-item codigo-item">
              <span class="info-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                  <rect x="14" y="14" width="3" height="3" />
                  <line x1="18" y1="14" x2="21" y2="14" />
                  <line x1="21" y1="17" x2="21" y2="21" />
                  <line x1="18" y1="21" x2="21" y2="21" />
                </svg>
              </span>
              <span class="info-label">Código</span>
              <span class="info-value codigo">{{ r.codigoRecogida }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FiltrosReservasGestor from "../components/FiltrosReservasGestor.vue";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
defineOptions({ name: "reservas-gestor-view" });

const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();

const reservas = ref(null);
const mensajeError = ref("");

// Función que obtiene todas las reservas realizadas en la aplicación
const getReservas = async () => {
  try {
    // Realiza una solicitud GET para obtener el historial de reservas
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

    const data = await response.json();
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

// Función para actualizar la lista de reservas mostradas en función de los filtros establecidos por el gestor
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
    if (filtros.usuario) {
      datos.usuario = filtros.usuario;
    }
    // Realiza una solicitud POST para filtrar las reservas
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

    const data = await response.json();
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getReservas();
});

// Función que obtiene el estado de las reservas
const getEstadoClass = (r) => {
  if (r.estado === "cancelada") return "cancelada";
  const ahora = new Date();
  const inicio = new Date(r.fechaInicio.replace(" ", "T"));
  const fin = new Date(r.fechaFin.replace(" ", "T"));
  if (fin < ahora) return "finalizada";
  if (inicio < ahora && fin > ahora) return "encurso";
  return "pendiente";
};

// Función que muestra el estado de las reservas
const getEstadoLabel = (r) => {
  const estado = getEstadoClass(r);
  return {
    cancelada: "Cancelada",
    finalizada: "Finalizada",
    encurso: "En curso",
    pendiente: "Pendiente",
  }[estado];
};

// Función para formatear la fecha
const formatFecha = (f) => {
  return new Date(f.replace(" ", "T")).toLocaleString("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.titulo-reservas-gestor {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 1rem;
}

.reservas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
  padding: 1.5rem 1rem;
  max-width: 1300px;
  margin: 0 auto;
}

.reserva-card {
  background: white;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.reserva-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.09);
}

.card-borde {
  height: 4px;
  width: 100%;
}

.reserva-card.encurso .card-borde {
  background: #16a34a;
}

.reserva-card.pendiente .card-borde {
  background: #2563eb;
}

.reserva-card.cancelada .card-borde {
  background: #dc2626;
}

.reserva-card.finalizada .card-borde {
  background: #9ca3af;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem 1.25rem 0.75rem;
  gap: 12px;
}

.ruta {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  flex: 1;
}

.lugar {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.lugar-destino {
  align-items: flex-end;
  text-align: right;
}

.ruta-flecha {
  color: #9ca3af;
  flex-shrink: 0;
}

.lugar-nombre {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  font-size: 16px;
  color: #111827;
  white-space: normal;
  overflow: visible;
  text-overflow: unset;
  word-break: keep-all;
  overflow-wrap: normal;
}

.lugar-anclaje {
  font-size: 14px;
  color: #6b7280;
  margin-top: 1px;
}

.etiqueta-estado {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 100px;
  white-space: nowrap;
  flex-shrink: 0;
}

.etiqueta-estado.encurso {
  background: #dcfce7;
  color: #166534;
}

.etiqueta-estado.pendiente {
  background: #dbeafe;
  color: #1e3a8a;
}

.etiqueta-estado.cancelada {
  background: #fee2e2;
  color: #991b1b;
}

.etiqueta-estado.finalizada {
  background: #f3f4f6;
  color: #4b5563;
}

.card-body {
  padding: 0.75rem 1.25rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-top: 1px solid #f3f4f6;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.info-icon {
  color: #9ca3af;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.info-label {
  color: #6b7280;
  min-width: 36px;
}

.info-value {
  color: #1f2937;
  font-weight: 500;
}

.codigo {
  font-family: "Courier New", monospace;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 13px;
  letter-spacing: 0.05em;
  color: #166534;
}

@media (min-width: 992px) {
  .lugar-nombre {
    font-size: 18px;
  }

  .lugar-anclaje {
    font-size: 14px;
  }

  .info-item {
    font-size: 14px;
  }

  .etiqueta-estado {
    font-size: 14px;
  }

  .codigo {
    font-size: 13px;
  }
}

@media (max-width: 576px) {
  .reservas-grid {
    grid-template-columns: 1fr;
    padding: 1rem 0.75rem;
  }

  .card-header {
    flex-direction: column;
    gap: 8px;
  }

  .etiqueta-estado {
    align-self: flex-start;
  }
}

#filtro-reserva-gestor {
  padding: 0 1rem;
}
</style>
