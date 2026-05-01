// src/stores/auth.js
import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({ token: null, usuario: null, rol: null }),

  actions: {
    setToken(newToken, usuario, rol) {
      this.token = newToken;
      this.usuario = usuario;
      this.rol = rol;
    },
    clearToken() {
      this.token = null;
      this.usuario = null;
      this.rol = null;
    },
  },
});
