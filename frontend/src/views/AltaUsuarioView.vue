<!-- src/views/AltaUsuarioView.vue-->
<template>
  <div id="alta-view" class="alta-container">
    <main>
      <div class="row justify-content-center mt-2">
        <div class="col-11 col-md-8 d-flex justify-content-center">
          <div class="card card-cibiuam">
            <h1 class="alta-title" data-cy="alta-tit">
              Alta de Usuario
              <span @click="mostrarAyuda = !mostrarAyuda" style="cursor: pointer">
                <img src="/ayuda.png" alt="Ayuda" class="icono" />
              </span>
            </h1>
            <p v-if="mostrarAyuda" class="instrucciones">
              Para crear una nueva cuenta, deberás introducir todos los campos
              solicitados a continuación. Una vez validados, el sistema le
              redirigirá a la pantalla de pago para poder finalizar la creación
              del nuevo usuario. Si alguno de los campos no fuese correcto, el
              sistema informará de los campos que deben corregirse.
            </p>
            <!-- Formulario alta de usuario -->
            <FormularioAlta @alta="enviarDatos" />
            <div class="contenedor">
              <div v-if="mensajeError" class="alert alert-danger">
                <p>
                  {{ mensajeError }} <br />
                  {{ camposErroneos }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Acceso directo a login -->
      <div class="d-flex flex-column justify-content-center">
        <div class="card card-cibiuam">
          <h3 class="aviso-registro">¿Ya estás registrado?</h3>
          <div class="enlace-login">
            <span><router-link to="/login">Accede</router-link></span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import FormularioAlta from "../components/FormularioAlta.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useDatosPago } from "@/stores/datosPago";
defineOptions({ name: "alta-view" });
const myVar = import.meta.env.VITE_DJANGOURL;
const router = useRouter();
const pagoStore = useDatosPago();
const mensajeError = ref("");
const camposErroneos = ref("");

// Función que se comunica con la API de Django para realizar el alta de un usuario
const enviarDatos = async (persona) => {
  try {
    // Realiza una solicitud POST para crear un usuario nuevo
    const response = await fetch(myVar + "/cibiuam/crear_usuario/", {
      method: "POST",
      body: JSON.stringify(persona),
      headers: { "Content-type": "application/json; charset=UTF-8" },
    });

    mensajeError.value = "";
    camposErroneos.value = "";

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error: ", errorData);
      mensajeError.value = errorData.Mensaje;

      // Construcción mensaje informativo de campos erróneos
      let campos = Object.keys(errorData.errores);
      if (campos.length > 0) {
        const indice = campos.indexOf("tlf");
        if (indice !== -1) {
          campos.splice(indice, 1);
          campos.push("teléfono");
        }
        let msg;
        if (campos.length === 0) {
          msg = "";
        } else if (campos.length === 1) {
          msg = campos[0];
        } else {
          const todosMenosUltimo = campos.slice(0, -1).join(", ");
          const ultimo = campos[campos.length - 1];
          msg = `${todosMenosUltimo} y ${ultimo}`;
        }
        camposErroneos.value = "Corrige los siguientes campos: " + msg + ".";
      }
      return;
    }

    // Guardamos respuesta de la API para continuar con el pago
    const data = await response.json();
    pagoStore.setPago(
      data.order_id,
      data.user_id,
      persona.usuario,
      data.importe,
      data.fin
    );

    // Redirigimos a la página de pago
    router.push("/pago_alta");
  } catch (error) {
    console.error(error);
  }
};

const mostrarAyuda = ref(false);
</script>

<style scoped>
.alta-container {
  width: 100%;
}

.card-cibiuam {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  text-align: center;
  border-top: 7px solid #0b6f0d;
  overflow: hidden;
  margin: 20px auto;
}

.alta-title {
  text-align: center;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.instrucciones {
  text-align: justify;
  margin: 0 auto 1rem auto;
}

.contenedor {
  display: flex;
  justify-content: center;
  margin-left: 1rem;
  margin-right: 1rem;
}

.aviso-registro {
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
}

.enlace-login {
  display: flex;
  flex-direction: column;
  font-size: 19px;
}

.enlace-login span {
  background: #eaf4e8;
  border-radius: 6px;
  padding: 10px 1px;
  line-height: 1.8;
  border: 2px solid black;
}

.icono {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}
</style>
