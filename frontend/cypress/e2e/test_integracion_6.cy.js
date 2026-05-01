// cypress/e2e/test_integracion_6.cy.js
describe("Test Integracion 6", () => {
  // Realiza las acciones de un usuario que desea realizar una reserva:
  // - Realiza login
  // - Realiza una reserva que finalmente no puede realizar
  // - Consulta sus reservas para cancelarla
  // - Cancela la reserva
  // - Consultamos reservas para ver que está cancelada
  // - Consultamos el perfil para ver que nos han reembolsado el importe
  // - Cierra sesión

  it("Acciones de un usuario registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    //Poblamos base de datos con datos iniciales necesarios
    cy.populate_integracion6();

    // Página inicio
    cy.visit("/");

    // Iniciamos sesión con los datos del usuario
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("usuario");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos al menú inicial
    cy.url().should("include", "/menu_usuario");

    // Comprobamos que muestra todas las opciones de funcionalidad del usuario
    cy.contains("¡Bienvenido, usuario!").should("be.visible");
    cy.contains("Consultar Estado del Campus").should("be.visible");
    cy.contains("Realizar Reserva").should("be.visible");
    cy.contains("Cancelar Reserva").should("be.visible");
    cy.contains("Mis Reservas").should("be.visible");
    cy.contains("Renovar Contrato").should("be.visible");
    cy.contains("usuario").should("be.visible");
    cy.contains("Notificaciones").should("be.visible");

    // Realizamos una reserva
    // Vamos a página de realizar reserva
    cy.get("[data-cy=reserva-page]").click();
    cy.url().should("include", "/realizar_reserva");

    // Rellenamos formulario de reserva
    const hoy = new Date().toISOString().split("T")[0];
    const ahora = new Date();

    // Hora Inicio
    const hInicio = new Date(ahora);
    hInicio.setMinutes(hInicio.getMinutes() + 90);

    // Hora Fin
    const hFin = new Date(ahora);
    hFin.setMinutes(hFin.getMinutes() + 100);

    const horaInicio = `${String(hInicio.getHours()).padStart(2, "0")}:${String(
      hInicio.getMinutes()
    ).padStart(2, "0")}`;
    const horaFin = `${String(hFin.getHours()).padStart(2, "0")}:${String(
      hFin.getMinutes()
    ).padStart(2, "0")}`;

    cy.get("[data-cy=select-reserva-origen]").select(
      "Facultad de Formación de Profesorado y Educación"
    );
    cy.get("[data-cy=select-reserva-destino]").select("EPS");
    cy.get("[data-cy=fechaInicio]").type(hoy);
    cy.get("[data-cy=horaInicio]").type(horaInicio);
    cy.get("[data-cy=fechaFin]").type(hoy);
    cy.get("[data-cy=horaFin]").type(horaFin);
    cy.get("[data-cy=reserva-boton]").click();

    // Debe redirigirnos al pago
    cy.url().should("include", "/pagar_reserva");

    // Información de pago
    cy.contains("Información general de la reserva").should("be.visible");
    cy.contains("Importe: 0.2€").should("be.visible");
    cy.contains("Inicio:").should("be.visible");
    cy.contains("Fin:").should("be.visible");
    cy.contains("Hora de Inicio:").should("be.visible");
    cy.contains("Hora de Fin:").should("be.visible");
    cy.contains("Origen:").should("be.visible");
    cy.contains("Destino:").should("be.visible");
    cy.contains(hoy).should("be.visible");
    cy.contains(horaInicio).should("be.visible");
    cy.contains(horaFin).should("be.visible");
    cy.contains("EPS").should("be.visible");
    cy.contains("Facultad de Formación de Profesorado y Educación").should(
      "be.visible"
    );

    // Simulamos reserva
    cy.populate_integracion6_1();

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Consultamos la reserva
    // Vamos a página de consultar reserva
    cy.get("[data-cy='/consultar_reservas']").click();
    cy.url().should("include", "/consultar_reservas");

    const formatFecha = (dateObj) => {
      return dateObj.toLocaleString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
        timeZone: "Europe/Madrid",
      });
    };

    cy.contains("Facultad de Formación de Profesorado y Educación").should(
      "be.visible"
    );
    cy.contains("EPS").should("be.visible");
    const fecha3 = new Date(ahora);
    fecha3.setMinutes(fecha3.getMinutes() + 90);
    const fecha4 = new Date(ahora);
    fecha4.setMinutes(fecha4.getMinutes() + 100);
    cy.contains(".etiqueta-estado", "Pendiente").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha3)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha4)).should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Cancelamos la reserva
    cy.get("[data-cy=cancelar-page]").click();
    cy.url().should("include", "/cancelar_reserva");
    cy.get("[data-cy='boton-2']").click();
    cy.get("[data-cy=cancelarReserva]").click();

    // Mensaje de reserva cancelada
    cy.get("[data-cy=msg]").should("exist");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Consultamos la reserva para confirmar que está cancelada
    // Vamos a página de consultar reserva
    cy.get("[data-cy='/consultar_reservas']").click();
    cy.url().should("include", "/consultar_reservas");

    cy.contains("Facultad de Formación de Profesorado y Educación").should(
      "be.visible"
    );
    cy.contains("EPS").should("be.visible");
    cy.contains(".etiqueta-estado", "Cancelada").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha3)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha4)).should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Consultamos nuestro perfil para ver si nos han reembolsado el importe
    cy.get("[data-cy='/consultar_perfil']").click();
    cy.url().should("include", "/consultar_perfil");
    cy.contains("Saldo Disponible:").should("be.visible");
    cy.contains("0.2€").should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");
  });
});
