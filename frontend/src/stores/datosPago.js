// src/stores/datosPago.js
import { defineStore } from "pinia";

export const useDatosPago = defineStore("pago", {
  state: () => ({
    order_id: null,
    user_id: null,
    usuario: null,
    importe: null,
    fin: null,
  }),

  actions: {
    setPago(order_id, user_id, usuario, importe, fin) {
      this.order_id = order_id;
      this.user_id = user_id;
      this.importe = importe;
      this.usuario = usuario;
      this.fin = fin;
    },
    clearPago() {
      this.order_id = null;
      this.user_id = null;
      this.usuario = null;
      this.importe = null;
      this.fin = null;
    },
  },
});
