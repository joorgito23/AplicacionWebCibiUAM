// src/stores/datosPagoRenovacion.js
import { defineStore } from "pinia";

export const useDatosPagoRenovacion = defineStore("pagoRenovacion", {
  state: () => ({
    order_id: null,
    user_id: null,
    usuario: null,
    importe: null,
    fin: null,
    tarifa: null,
  }),

  actions: {
    setPago(order_id, user_id, usuario, importe, fin, tarifa) {
      this.order_id = order_id;
      this.user_id = user_id;
      this.importe = importe;
      this.usuario = usuario;
      this.fin = fin;
      this.tarifa = tarifa;
    },
    clearPago() {
      this.order_id = null;
      this.user_id = null;
      this.usuario = null;
      this.importe = null;
      this.fin = null;
      this.tarifa = null;
    },
  },
});
