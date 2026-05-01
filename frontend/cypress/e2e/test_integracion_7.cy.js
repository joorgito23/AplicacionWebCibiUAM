// cypress/e2e/test_integracion_7.cy.js
describe("Test Integracion 7", () => {
  // Realiza las acciones de un gestor que desea consultar el historial de reservas de los usuarios para gestionar el servicio:
  // - Realiza login
  // - Consulta el historial de reservas general
  // - Filtra las reservas para analizar la demanda
  // - Crea una nueva estación en una zona transitada
  // - Cierra sesión

  it("Acciones de un gestor registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    //Poblamos base de datos con datos iniciales necesarios
    cy.populate_integracion7();

    // Página inicio
    cy.visit("/");

    // Iniciamos sesión con los datos del usuario
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("gestor");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_gestor");

    // Comprobamos que muestra todas las opciones de funcionalidad del gestor
    cy.contains("Consultar Estado de Bicicletas y Estaciones").should(
      "be.visible"
    );
    cy.contains("Alta de Estación").should("be.visible");
    cy.contains("Alta de Bicicleta").should("be.visible");
    cy.contains("Reservas").should("be.visible");
    cy.contains("Contratos").should("be.visible");
    cy.contains("Actualizar Tarifas").should("be.visible");

    // Consultamos la reserva
    // Vamos a página de consultar reservas
    cy.get("[data-cy='/consultar_reservas_gestor']").click();
    cy.url().should("include", "/consultar_reservas_gestor");

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

    // Filtramos por estación de origen
    cy.get("[data-cy=select-reserva-origen]").select("Estación 2");
    cy.get("[data-cy=filtrar-boton]").click();

    cy.contains("Estación 2").should("be.visible");
    cy.contains("Estación 1").should("be.visible");
    const ahora = new Date();
    const fecha3 = new Date(ahora);
    fecha3.setDate(fecha3.getDate() + 2);
    const fecha4 = new Date(ahora);
    fecha4.setDate(fecha4.getDate() + 2);
    fecha4.setMinutes(fecha4.getMinutes() + 10);
    cy.contains(".etiqueta-estado", "Pendiente").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha3)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha4)).should("be.visible");
    cy.contains(".info-value", "usuario2").should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_gestor']").click();
    cy.url().should("include", "/menu_gestor");

    // Damos de alta una estacion
    // Vamos a página de alta de estacion
    cy.get("[data-cy=est-page]").click();
    cy.url().should("include", "/alta_estacion");
    cy.get("[data-cy=titulo-alta-est]").should("exist");

    // Rellena formulario
    cy.get("[data-cy=est-nombre]").type("Renfe");
    cy.get("[data-cy=est-ubicacion]").type("Fuencarral-El Pardo, 28049 Madrid");
    cy.get("[data-cy=est-anc]").type(4);
    cy.get("[data-cy=est-lat]").type("40.54398922412274");
    cy.get("[data-cy=est-long]").type("-3.7002395471394287");

    // Pulsa botón de alta
    cy.get("[data-cy=alta-est-boton]").click();
    cy.get("[data-cy=msg]").should("exist");
    cy.wait(6000);

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");
  });
});
