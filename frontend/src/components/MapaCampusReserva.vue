<!-- src/componets/MapaCampusReserva.vue -->
<template>
  <div id="mapa-reserva">
    <div class="map-container">
      <div id="map"></div>
      <div class="map-atribucion">
        ©
        <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors
      </div>
      <button v-if="
        !authStore.token || (authStore.token && authStore.rol === 'usuario')
      " class="map-location-btn" @click="localizar">
        <img src="/mapaUbi.png" alt="Ubi" class="icono" />
      </button>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "mapa-reserva" });
import { shallowRef, ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useAuthStore } from "@/stores/auth";
const myVar = import.meta.env.VITE_DJANGOURL;

const estaciones = ref([]);
const map = shallowRef(null);
const authStore = useAuthStore();
// Función para renderizar el mapa en la pantalla
const mapa = async () => {
  // Coordenadas del campus de la UAM
  const campusCenter = [40.54460831359694, -3.6977858789107554];

  // Crea el mapa
  map.value = L.map("map").setView(campusCenter, 16);

  // Incluye la capa de OpenStreetMap
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map.value);

  setTimeout(() => {
    map.value.invalidateSize();
  }, 100);

  // Crea un marcador de la sede de CibiUAM
  L.marker([40.54377187669374, -3.7000215711646707], { title: "CibiUAM" })
    .addTo(map.value)
    .bindPopup(
      `
        <div>
            <img src="/sede.png" alt="Sede" style="width:24px; height:24px;">
            <b>Sede CibiUAM</b>
        </div>
      `
    )
    .openPopup();

  try {
    // Realiza una solicitud GET para obtener las estaciones disponibles
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      return;
    }

    const data = await response.json();
    // Guarda las estaciones
    estaciones.value = data;
  } catch (error) {
    console.error(error);
  }

  // Para cada estación crea un marcador en el mapa
  for (let i = 0; i < estaciones.value.length; i++) {
    // Creación del marcador
    L.marker(
      [
        Number(estaciones.value[i].latitud),
        Number(estaciones.value[i].longitud),
      ],
      { title: estaciones.value[i].ubicacion }
    ).addTo(map.value).bindPopup(`
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <img src="/parking-de-bicicletas.png" alt="Parking" style="width:24px; height:24px;">
                <b>${estaciones.value[i].nombre}</b>
            </div>
            `);
  }

  // Geolocalización
  map.value.on("locationfound", (e) => {
    L.marker(e.latlng)
      .addTo(map.value)
      .bindPopup("Usted está aquí")
      .openPopup();
  });

  map.value.on("locationerror", () => {
    alert("No se pudo obtener la ubicación");
  });
};

onMounted(() => {
  mapa();
});

// Función que obtiene la ubicación del usuario
const localizar = async () => {
  map.value.locate({
    setView: true,
    maxZoom: 16,
  });
};
</script>

<style scoped>
.map-container {
  width: 95%;
  max-width: 900px;
  margin: 1.5rem auto;
}

#map {
  height: 500px;
  width: 100%;
  border-radius: 12px;
}

.map-atribucion {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background: rgba(255, 255, 255, 0.8);
  padding: 2px 6px;
  font-size: 11px;
  border-radius: 4px;
  z-index: 1000;
  font-weight: bold;
}

.leaflet-pane img {
  max-width: none !important;
  height: auto !important;
}

.map-location-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  border-radius: 6px;
  padding: 8px;
  cursor: pointer;
  font-size: 18px;
  z-index: 1000;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.map-location-btn:hover {
  background: #f0f0f0;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}
</style>
