import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AltaUsuarioView from "../views/AltaUsuarioView.vue";
import IniciarSesionView from "../views/IniciarSesionView.vue";
import ConsultarEstadoView from "../views/ConsultarEstadoView.vue";
import MenuUsuarioView from "../views/MenuUsuarioView.vue";
import CancelarReservaView from "../views/CancelarReservaView.vue";
import ConsultarPerfilView from "../views/ConsultarPerfilView.vue";
import ConsultarReservasView from "../views/ConsultarReservasView.vue";
import LeerNotificacionesView from "../views/LeerNotificacionesView.vue";
import RealizarReservaView from "../views/RealizarReservaView.vue";
import RenovarContratoView from "../views/RenovarContratoView.vue";
import PagoAltaUsuarioView from "../views/PagoAltaUsuarioView.vue";
import PagarRenovacionView from "../views/PagarRenovacionView.vue";
import ConsultarEstadoGestorView from "../views/ConsultarEstadoGestorView.vue";
import MenuGestorView from "../views/MenuGestorView.vue";
import MenuAdminView from "../views/MenuAdminView.vue";
import AltaEstacionView from "../views/AltaEstacionView.vue";
import AltaBiciView from "../views/AltaBiciView.vue";
import ConsultarContratosView from "../views/ConsultarContratosView.vue";
import ActualizarTarifasView from "../views/ActualizarTarifasView.vue";
import FAQView from "../views/FAQView.vue";
import PagoReservaView from "../views/PagoReservaView.vue";
import ConsultarReservasGestorView from "../views/ConsultarReservasGestorView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        headerLinks: [
          { to: "/login", text: "Acceder" },
          { to: "/alta_usuario", text: "Registrarse" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
        ],
      },
    },
    {
      path: "/alta_usuario",
      name: "alta_usuario",
      component: AltaUsuarioView,
      meta: {
        headerLinks: [
          { to: "/login", text: "Acceder" },
          { to: "/alta_usuario", text: "Registrarse" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
          { to: "/", text: "Inicio" },
        ],
      },
    },
    {
      path: "/login",
      name: "login",
      component: IniciarSesionView,
      meta: {
        headerLinks: [
          { to: "/login", text: "Acceder" },
          { to: "/alta_usuario", text: "Registrarse" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
          { to: "/", text: "Inicio" },
        ],
      },
    },
    {
      path: "/consultar_estado",
      name: "consultar_estado",
      component: ConsultarEstadoView,
      meta: {
        headerLinksLogout: [
          { to: "/login", text: "Acceder" },
          { to: "/alta_usuario", text: "Registrarse" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
          { to: "/", text: "Inicio" },
        ],
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/menu_usuario",
      name: "menu_usuario",
      component: MenuUsuarioView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/cancelar_reserva",
      name: "cancelar_reserva",
      component: CancelarReservaView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/consultar_perfil",
      name: "consultar_perfil",
      component: ConsultarPerfilView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/consultar_reservas",
      name: "consultar_reservas",
      component: ConsultarReservasView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/consultar_reservas_gestor",
      name: "consultar_reservas_gestor",
      component: ConsultarReservasGestorView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/leer_notificaciones",
      name: "leer_notificaciones",
      component: LeerNotificacionesView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/realizar_reserva",
      name: "realizar_reserva",
      component: RealizarReservaView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/pagar_reserva",
      name: "pagar_reserva",
      component: PagoReservaView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/renovar_contrato",
      name: "renovar_contrato",
      component: RenovarContratoView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/pago_alta",
      name: "pago_alta",
      component: PagoAltaUsuarioView,
      meta: {
        headerLinksLogout: [
          { to: "/login", text: "Acceder" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
          { to: "/", text: "Inicio" },
        ],
      },
    },
    {
      path: "/pagar_renovacion",
      name: "pagar_renovacion",
      component: PagarRenovacionView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_perfil", text: "👤 Mi Perfil" },
          { to: "/leer_notificaciones", text: "✉️ Notificaciones" },
          { to: "/consultar_reservas", text: "Mis Reservas" },
          { to: "/menu_usuario", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/menu_gestor",
      name: "menu_gestor",
      component: MenuGestorView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/menu_admin",
      name: "menu_admin",
      component: MenuAdminView,
      meta: {
        headerLinksLogin: [
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/consultar_estado_gestor",
      name: "consultar_estado_gestor",
      component: ConsultarEstadoGestorView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/alta_estacion",
      name: "alta_estacion",
      component: AltaEstacionView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/alta_bicicleta",
      name: "alta_bicicleta",
      component: AltaBiciView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/consultar_contratos",
      name: "consultar_contratos",
      component: ConsultarContratosView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/actualizar_tarifas",
      name: "actualizar_tarifas",
      component: ActualizarTarifasView,
      meta: {
        headerLinksLogin: [
          { to: "/consultar_contratos", text: "Contratos" },
          { to: "/consultar_reservas_gestor", text: "Reservas" },
          { to: "/menu_gestor", text: "Inicio" },
          { text: "Cerrar Sesión", action: "logout", to: "/" },
        ],
      },
    },
    {
      path: "/faq",
      name: "faq",
      component: FAQView,
      meta: {
        headerLinks: [
          { to: "/login", text: "Acceder" },
          { to: "/alta_usuario", text: "Registrarse" },
          { to: "/consultar_estado", text: "Conoce el campus" },
          { to: "/faq", text: "FAQ" },
          { to: "/", text: "Inicio" },
        ],
      },
    },
  ],
  scrollBehavior() {
    // Siempre ir al inicio de la página al cambiar de ruta
    return { left: 0, top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  // Si la ruta no es la inicial y no venimos de otra url, redirige a la inicial
  if (to.name !== "home" && !from.name) {
    return next({ name: "home" });
  }
  next();
});

export default router;
