<!-- src/views/ConsultarContratosView.vue -->
<template>
  <div id="contratos-view" style="width: 100%">
    <main>
      <h1 class="titulo-contrato" data-cy="contrato-title">
        Contratos del Sistema
      </h1>
      <!-- Filtros de los contratos -->
      <FiltrosContratos @filtrar-contratos="actualizarContratos" />
      <!-- Tarjetas de contratos -->
      <div class="reservas-grid">
        <div v-for="c in contratos" :key="c.id" class="reserva-card" :class="getEstadoContratoClass(c)">
          <div class="card-borde"></div>
          <div class="card-header">
            <div class="ruta">
              <div class="lugar">
                <span class="lugar-nombre">{{ c.usuario.usuario.username }}</span>
                <span class="lugar-tarifa">Tarifa {{ c.tarifa.duracion }}</span>
              </div>
            </div>
            <span :class="['etiqueta-estado', getEstadoContratoClass(c)]">
              {{ getEstadoContratoLabel(c) }}
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
              <span class="info-value">{{ formatFecha(c.inicio) }}</span>
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
              <span class="info-value">{{ formatFecha(c.fin) }}</span>
            </div>
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

// Función para obtener el estado del contrato
const getEstadoContratoClass = (c) => {
  const ahora = new Date();
  const inicio = new Date(c.inicio);
  const fin = new Date(c.fin);
  if (fin < ahora) return "finalizado";
  if (inicio > ahora) return "pendiente";
  return "encurso";
};

// Función para mostrar el estado del contrato
const getEstadoContratoLabel = (c) => {
  const estado = getEstadoContratoClass(c);
  return {
    finalizado: "Finalizado",
    pendiente: "Pendiente de inicio",
    encurso: "Activo",
  }[estado];
};

// Función para dar formato a la fecha del contrato
const formatFecha = (f) => {
  return new Date(f.replace(" ", "T")).toLocaleString("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};
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

.reserva-card.finalizado .card-borde {
  background: #dc2626;
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
  word-break: break-word;
}

.lugar-tarifa {
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

.etiqueta-estado.finalizado {
  background: #fee2e2;
  color: #991b1b;
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

  .lugar-tarifa {
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

#filtros-contratos {
  padding: 0 1rem;
}
</style>
