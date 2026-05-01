import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";

import "./assets/main.css";
import router from "./router";
const myapp = createApp(App);
const pinia = createPinia();

myapp.use(pinia);
myapp.use(router);
myapp.mount("#app");

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
