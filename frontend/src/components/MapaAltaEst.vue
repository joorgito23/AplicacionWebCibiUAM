<!-- src/components/MapaAltaEst.vue -->
<template>
  <div id="mapa-est">
    <div class="map-container">
      <div id="map"></div>
      <div class="map-atribucion">
        ©
        <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors,
        geocoding by
        <a href="https://nominatim.openstreetmap.org/">Nominatim</a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: "mapa-est" });
import { shallowRef, ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
const myVar = import.meta.env.VITE_DJANGOURL;
const estaciones = ref([]);
const map = shallowRef(null);

// Función para renderizar el mapa en la pantalla
const mapa = async () => {
  // Coordenadas del campus
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

  // Crea un marcador para la sede de CibiUAM
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
    // Realiza una solicitud GET para obtener las estaciones del campus
    const response = await fetch(myVar + "/cibiuam/informacion/estaciones/");

    if (!response.ok) {
      return;
    }

    const data = await response.json();
    estaciones.value = data;
  } catch (error) {
    console.error(error);
  }

  // Crea un marcador para cada estación
  for (let i = 0; i < estaciones.value.length; i++) {
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

  // Interacción con el mapa al hacer click en un punto para mostrar coordenadas y ubicación exacta
  const popup = L.popup();
  map.value.on("click", async (e) => {
    const { lat, lng } = e.latlng;
    let direccion = "No disponible";

    // Petición a Nominatim para obtener ubicación dadas las coordenadas
    try {
      const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`;
      const res = await fetch(url);
      const data = await res.json();
      direccion = data.display_name || direccion;
    } catch (error) {
      console.error("Error obteniendo dirección:", error);
    }

    // Creación del PopUp a mostrar con las coordenadas y la ubicación deseada
    popup
      .setLatLng([lat, lng])
      .setContent(
        `<b>Latitud:</b> ${lat.toFixed(5)}<br>` +
        `<b>Longitud:</b> ${lng.toFixed(5)}<br>` +
        `<b>Dirección:</b> ${direccion}`
      )
      .openOn(map.value);
  });
};

onMounted(() => {
  mapa();
});
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
</style>
