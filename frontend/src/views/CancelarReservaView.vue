<!-- src/views/CancelarReservaView.vue -->
<template>
  <div id="cancelar-view" style="width: 100%">
    <main>
      <h1 class="titulo-cancelar" data-cy="cancelar-title">
        Cancelación de Reservas
        <span @click="mostrarAyuda = !mostrarAyuda" style="cursor: pointer">
          <img src="/ayuda.png" alt="Ayuda" class="icono" />
        </span>
      </h1>
      <div class="row justify-content-center mt-3">
        <div class="col-11 col-md-8 d-flex justify-content-center mb-1">
          <p v-if="mostrarAyuda" class="instrucciones">
            A continuación podrá consultar todas las reservas pendientes de
            realización para su cancelación. Para ello, deberá marcar la opción
            de cancelar en la reserva que desee cancelar.
          </p>
        </div>
      </div>
      <!-- Tarjetas de reservas disponibles para cancelar -->
      <div class="reservas-grid">
        <div v-for="r in reservas" :key="r.id" v-show="new Date(r.fechaInicio.replace(' ', 'T')) >= new Date() &&
          r.estado !== 'cancelada'
          " class="reserva-card" :class="getEstadoClass(r)">
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
            <div class="info-item">
              <span class="info-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                  <rect x="14" y="14" width="3" height="3" />
                </svg>
              </span>
              <span class="info-label">ID</span>
              <span class="info-value">{{ r.id }}</span>
            </div>
          </div>

          <div class="card-footer">
            <button class="btn-cancelar" @click="abrirModal(r.id)" :data-cy="'boton-' + r.id">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              Cancelar reserva
            </button>
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
      <div v-if="mostrarModal" class="modal-overlay" @click.self="mostrarModal = false">
        <div class="modal-confirmacion">
          <h4>¿Cancelar reserva con id {{ reservaCancelar }}?</h4>
          <p>Esta acción no se puede deshacer.</p>
          <div class="modal-actions">
            <button class="btn-secundario" @click="mostrarModal = false">
              Volver
            </button>
            <button class="btn-cancelar" @click="cancelar" data-cy="cancelarReserva">
              Sí, cancelar
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: "cancelar-view" });
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
const myVar = import.meta.env.VITE_DJANGOURL;
const authStore = useAuthStore();
const reservas = ref([]);
const mostrarAyuda = ref(false);
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
    // Guarda las reservas para mostrar al usuario mediante tarjetas
    reservas.value = data;
  } catch (error) {
    console.error(error);
  }
};

const mensajeError = ref("");
const mensaje = ref("");
const mostrarModal = ref(false);
const reservaCancelar = ref(null);

// Función para abrir la confirmación
const abrirModal = (id) => {
  reservaCancelar.value = id;
  mostrarModal.value = true;
};

// Función que cancela una reserva del usuario
const cancelar = async () => {
  try {
    // Realiza una solicitud POST para cancelar la reserva
    const datos = {
      reserva_id: reservaCancelar.value,
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
      mostrarModal.value = false;
      reservaCancelar.value = null;
      return;
    }

    const data = await response.json();
    mensaje.value = data.Mensaje;
    setTimeout(() => {
      mensaje.value = "";
    }, 3000);

    // Obtiene las reservas actualizadas tras la cancelación
    getReservas();

    mostrarModal.value = false;
    reservaCancelar.value = null;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getReservas();
});

// Función que devuelve el estado de la reserva
const getEstadoClass = (r) => {
  if (r.estado === "cancelada") return "cancelada";
  const ahora = new Date();
  const inicio = new Date(r.fechaInicio.replace(" ", "T"));
  const fin = new Date(r.fechaFin.replace(" ", "T"));
  if (fin < ahora) return "finalizada";
  if (inicio < ahora && fin > ahora) return "encurso";
  return "pendiente";
};

// Función para mostrar el estado correcto de la reserva
const getEstadoLabel = (r) => {
  const estado = getEstadoClass(r);
  return {
    cancelada: "Cancelada",
    finalizada: "Finalizada",
    encurso: "En curso",
    pendiente: "Pendiente",
  }[estado];
};

// Función para dar formato a la fecha de la reserva
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
  display: flex;
  flex-direction: column;
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
  word-break: break-word;
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
  flex: 1;
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

.card-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #f3f4f6;
  margin-top: auto;
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
  transition: background 0.2s ease, border-color 0.2s ease, transform 0.1s ease;
}

.btn-cancelar:hover {
  background: #fee2e2;
  border-color: #dc2626;
  transform: translateY(-1px);
}

.btn-cancelar:active {
  transform: translateY(0);
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 2rem;
  margin-right: 2rem;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
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
</style>
