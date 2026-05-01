// src/stores/datosPagoReserva.js
import { defineStore } from "pinia";

export const useDatosPagoReserva = defineStore("pagoReserva", {
  state: () => ({
    order_id: null,
    reserva_id: null,
    saldo: null,
    importe: null,
    inicio: null,
    fin: null,
    horaInicio: null,
    horaFin: null,
    origen: null,
    destino: null,
  }),

  actions: {
    setPago(
      order_id,
      reserva_id,
      saldo,
      importe,
      inicio,
      fin,
      horaInicio,
      horaFin,
      origen,
      destino
    ) {
      this.order_id = order_id;
      this.reserva_id = reserva_id;
      this.saldo = saldo;
      this.importe = importe;
      this.inicio = inicio;
      this.fin = fin;
      this.horaInicio = horaInicio;
      this.horaFin = horaFin;
      this.origen = origen;
      this.destino = destino;
    },
    clearPago() {
      this.order_id = null;
      this.reserva_id = null;
      this.saldo = null;
      this.importe = null;
      this.inicio = null;
      this.fin = null;
      this.horaInicio = null;
      this.horaFin = null;
      this.origen = null;
      this.destino = null;
    },
  },
});
