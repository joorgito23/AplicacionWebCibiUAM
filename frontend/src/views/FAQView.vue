<!-- src/views/FAQView.vue -->
<template>
  <div id="faq">
    <main>
      <div class="container my-5">
        <h1 class="titulo-faq text-center mb-5">
          Frequently Asked Questions (FAQ)
        </h1>
        <div class="row justify-content-center g-4">
          <div v-for="(faq, index) in faqs" :key="index" class="col-12 col-md-10 col-lg-8">
            <div class="faq-item p-4 shadow-sm" @click="marcar(index)">
              <div class="d-flex justify-content-between align-items-center faq-header">
                <h5 class="faq-question mb-0">{{ faq.question }}</h5>
                <span :class="['arrow', { open: indicesActivos.includes(index) }]">▼</span>
              </div>
              <transition name="fade">
                <h6 v-if="indicesActivos.includes(index)" class="faq-answer mt-3">
                  {{ faq.answer }}
                </h6>
              </transition>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";

const indicesActivos = ref([]);

// Función para mantener los índices de las preguntas ampliadas
const marcar = (index) => {
  if (indicesActivos.value.includes(index)) {
    indicesActivos.value = indicesActivos.value.filter((i) => i !== index);
  } else {
    indicesActivos.value.push(index);
  }
};

const faqs = [
  {
    question: "¿En qué consiste este proyecto?",
    answer:
      "Este proyecto tiene como objetivo servir como punto de partida para la reapertura y modernización de CibiUAM mediante la realización de una aplicación web que permita la reserva de bicicletas en el campus de la UAM.",
  },
  {
    question: "¿Cómo surgió este proyecto?",
    answer:
      "Este proyecto surge como propuesta de TFG del Grado en Ingeniería Informática y ha sido realizado por Jorge Pedraza Ortega.",
  },
  {
    question: "¿Cuál es la necesidad de esta aplicación?",
    answer:
      "Esta aplicación pretende modernizar el proceso de reserva de bicicletas de CibiUAM sustituyendo a los formularios físicos tradicionales que existían anteriormente de manera que permita a los usuarios realizar una reserva rápida desde cualquier ubicación. La aplicación pretende ofrecer un diseño minimalista, simple y fácil de usar.",
  },
  {
    question: "¿Qué ofrece la aplicación a los usuarios no registrados?",
    answer:
      "La aplicación cuenta con un modo invitado para que los usuarios interesados puedan conocer las tarifas del servicio y el estado del campus en tiempo real.",
  },
  {
    question: "¿Cómo puedo darme de alta en el servicio?",
    answer:
      'Para darse de alta, deberás acceder al apartado "Registarse" y rellenar los campos solicitados. Posteriormente, será redirigido a la plataforma externa de pago PayPal para realizar el pago de la tarifa deseada. Una vez completado, podrá hacer uso del servicio cuando desee.',
  },
  {
    question: "¿Qué acciones puede realizar el usuario registrado?",
    answer:
      "En el menú del usuario, podrá consultar el estado del campus en tiempo real para conocer el número de bicicletas y anclajes disponibles en cada estación, además de  realizar y cancelar una reserva, consultar las reservas realizadas, renovar su contrato, consultar y actualizar su perfil de usuario y leer las notificaciones recibidas.",
  },
  {
    question: "¿Cómo realizo una reserva?",
    answer:
      "Para realizar una reserva, deberá introducir las estaciones de origen y destino deseadas, así como la franja horaria en la que desea reservar la bicicleta. Una vez validados los datos, procederá al pago para confirmar su reserva. Tras la realización de la reserva, recibirá una notificación con toda la información de la reserva realizada.",
  },
  {
    question: "¿Cómo cancelo una reserva?",
    answer:
      "Podrá cancelar una reserva una hora antes de su inicio. Para ello, deberá seleccionar la reserva a cancelar y recibirá un reembolso del importe de la reserva a su cuenta para que pueda usarlo en futuras reservas que realice.",
  },
  {
    question: "¿Cómo renuevo el contrato?",
    answer:
      "En su perfil, podrá consultar la fecha de finalización de su contrato. Además, recibirá 10 días antes de su finalización una notificación informativa. Para renovar el contrato, deberá introducir la tarifa deseada y proceder al pago de la cuota de uso seleccionada. Una vez realizado el pago, su fecha de fin de contrato será ampliada automáticamente.",
  },
];
</script>

<style scoped>
.titulo-faq {
  font-family: "DM Sans", sans-serif;
  font-weight: 700;
  font-size: 2.5rem;
  color: #4a4a4a;
}

.faq-item {
  background: #ffffff;
  border-radius: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.faq-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  background-color: #f8f9ff;
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.faq-question {
  font-weight: 600;
  font-size: 1.125rem;
  color: #333333;
}

.arrow {
  font-size: 1.25rem;
  color: #4a7729;
  transition: transform 0.3s ease;
}

.arrow.open {
  transform: rotate(180deg);
}

.faq-answer {
  margin-top: 0.8rem;
  color: #555555;
  line-height: 1.7;
  font-size: 1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 768px) {
  .titulo-faq {
    font-size: 2rem;
  }

  .faq-question {
    font-size: 1rem;
  }
}
</style>
