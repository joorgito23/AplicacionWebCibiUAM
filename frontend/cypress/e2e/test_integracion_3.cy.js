// cypress/e2e/test_integracion_3.cy.js
describe("Test Integracion 3", () => {
  // Realiza las acciones cotidianas de un gestor que desea gestionar el servicio:
  // - Realiza login
  // - Consulta el estado de las bicicletas y estaciones
  // - Da de alta una estación
  // - Da de alta una bicicleta
  // - Consulta el historial de contratos
  // - Filtra los contratos
  // - Actualiza el precio de las tarifas
  // - Realiza logout

  it("Acciones de un gestor registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    // Poblamos la base de datos con los datos iniciales necesarios
    cy.populate_integracion3();

    // Página inicio
    cy.visit("/");

    // Iniciamos sesión con los datos del gestor
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("gestor");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos al menú inicial
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

    // Consultamos el estado de las bicicletas y estaciones
    // Vamos a página de consultar estado
    cy.get("[data-cy=estado-gestor-page]").click();
    cy.url().should("include", "/consultar_estado_gestor");
    cy.wait(1000);

    // EPS
    cy.contains("Estación EPS").should("be.visible");
    cy.contains(
      "Ubicación: Campus de Cantoblanco, C. Francisco Tomás y Valiente, 11, Fuencarral-El Pardo, 28049 Madrid"
    ).should("be.visible");
    cy.contains("Bicicletas disponibles: 0").should("be.visible");
    cy.contains("Anclajes libres: 2").should("be.visible");

    // Facultad de Formación de Profesorado y Educación
    cy.get("[data-cy=siguienteEst]").click();
    cy.contains(
      "Estación Facultad de Formación de Profesorado y Educación"
    ).should("be.visible");
    cy.contains(
      "Ubicación: C. Francisco Tomás y Valiente, 3, Fuencarral-El Pardo, 28049 Madrid"
    ).should("be.visible");
    cy.contains("Bicicletas disponibles: 2").should("be.visible");
    cy.contains("Anclajes libres: 1").should("be.visible");

    // Consultamos disponibilidad de bicicletas

    cy.get("[data-cy=estado-bicis]").click();
    cy.wait(1000);

    // Bicicleta 1
    cy.contains("Bicicleta con id 1").should("be.visible");
    cy.contains(
      "Estado: Bicicleta ubicada en el anclaje número 1 de la estación Facultad de Formación de Profesorado y Educación."
    ).should("be.visible");

    // Bicicleta 2
    cy.get("[data-cy=anteriorBici]").click();
    cy.contains("Bicicleta con id 2").should("be.visible");
    cy.contains(
      "Estado: Bicicleta ubicada en el anclaje número 2 de la estación Facultad de Formación de Profesorado y Educación."
    ).should("be.visible");

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

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_gestor");

    // Damos de alta una bicicleta
    // Vamos a página de alta de bicicleta
    cy.get("[data-cy=bici-page]").click();
    cy.url().should("include", "/alta_bicicleta");
    cy.get("[data-cy=bici-title]").should("exist");

    // Comprobamos que nos permite seleccionar las estaciones existentes
    cy.get("[data-cy=select-est]")
      .contains("option", "-- Estación --")
      .should("exist");
    cy.get("[data-cy=select-est]").contains("option", "EPS").should("exist");
    cy.get("[data-cy=select-est]")
      .contains("option", "Facultad de Formación de Profesorado y Educación")
      .should("exist");
    cy.get("[data-cy=select-est]").contains("option", "Renfe").should("exist");

    // Seleccionamos estación renfe
    cy.get("[data-cy=select-est]").select("Renfe");

    // Comprobamos que nos permite seleccionar los anclajes existentes
    cy.get("[data-cy=select-anc]")
      .contains("option", "-- Anclaje --")
      .should("exist");
    cy.get("[data-cy=select-anc]").contains("option", "1").should("exist");
    cy.get("[data-cy=select-anc]").contains("option", "2").should("exist");
    cy.get("[data-cy=select-anc]").contains("option", "3").should("exist");
    cy.get("[data-cy=select-anc]").contains("option", "4").should("exist");

    // Seleccionamos anclaje 1
    cy.get("[data-cy=select-anc]").select("1");

    // Pulsa botón de alta
    cy.get("[data-cy=alta-bici-boton]").click();
    cy.get("[data-cy=msg]").should("exist");
    cy.wait(6000);

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_gestor");

    // Consultamos contratos
    // Vamos a página de consulta de contratos
    cy.get("[data-cy='/consultar_contratos']").click();
    cy.url().should("include", "/consultar_contratos");
    cy.get("[data-cy=contrato-title]").should("exist");

    const formatFecha = (dateObj) => {
      return dateObj.toLocaleString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        timeZone: "Europe/Madrid",
      });
    };

    const hoy = new Date();
    const fecha = new Date(hoy);
    fecha.setDate(hoy.getDate() - 180);
    const fecha2 = new Date(hoy);
    fecha2.setDate(hoy.getDate() - 1);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa semestral").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha2)).should("be.visible");
    cy.contains(".etiqueta-estado", "Finalizado").should("be.visible");

    const fecha3 = new Date(hoy);
    fecha3.setDate(hoy.getDate() + 30 * 6);
    const fecha4 = new Date(hoy);
    fecha4.setDate(hoy.getDate() + 30 * 18 - 1);

    cy.contains(".lugar-nombre", "usuario2").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa anual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha3)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha4)).should("be.visible");
    cy.contains(".etiqueta-estado", "Pendiente de inicio").should("be.visible");

    const fecha5 = new Date(hoy);
    fecha5.setDate(hoy.getDate());
    const fecha6 = new Date(hoy);
    fecha6.setDate(hoy.getDate() + 29);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa mensual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha5)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha6)).should("be.visible");
    cy.contains(".etiqueta-estado", "Activo").should("be.visible");

    // Filtramos contratos

    // Vemos que podemos escoger cualquier tarifa
    cy.get("[data-cy=select-tarifa]")
      .contains("option", "Todas las tarifas")
      .should("exist");
    cy.get("[data-cy=select-tarifa]")
      .contains("option", "mensual")
      .should("exist");
    cy.get("[data-cy=select-tarifa]")
      .contains("option", "anual")
      .should("exist");
    cy.get("[data-cy=select-tarifa]")
      .contains("option", "semestral")
      .should("exist");

    // Filtramos por tarifa
    cy.get("[data-cy=select-tarifa]").select("mensual");
    cy.get("[data-cy=filtrar-boton]").click();

    const fecha7 = new Date(hoy);
    fecha7.setDate(hoy.getDate());
    const fecha8 = new Date(hoy);
    fecha8.setDate(hoy.getDate() + 29);
    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa mensual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha7)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha8)).should("be.visible");
    cy.contains(".etiqueta-estado", "Activo").should("be.visible");

    // Filtramos por inicio
    cy.get("[data-cy=select-tarifa]").select("");
    const fecha9 = new Date(hoy);
    fecha9.setDate(hoy.getDate());
    cy.get("[data-cy=inicio]").type(fecha9.toISOString().slice(0, 10));
    cy.get("[data-cy=filtrar-boton]").click();

    const fecha10 = new Date(hoy);
    fecha10.setDate(hoy.getDate() + 30 * 6);
    const fecha11 = new Date(hoy);
    fecha11.setDate(hoy.getDate() + 30 * 18 - 1);

    cy.contains(".lugar-nombre", "usuario2").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa anual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha10)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha11)).should("be.visible");
    cy.contains(".etiqueta-estado", "Pendiente de inicio").should("be.visible");

    const fecha12 = new Date(hoy);
    fecha12.setDate(hoy.getDate());
    const fecha13 = new Date(hoy);
    fecha13.setDate(hoy.getDate() + 29);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa mensual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha12)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha13)).should("be.visible");
    cy.contains(".etiqueta-estado", "Activo").should("be.visible");

    // Filtramos por fin
    cy.get("[data-cy=select-tarifa]").select("");
    const fecha14 = new Date(hoy);
    fecha14.setDate(hoy.getDate() - 5000);
    cy.get("[data-cy=inicio]").type(fecha14.toISOString().slice(0, 10));

    const fecha15 = new Date(hoy);
    fecha15.setDate(hoy.getDate());
    cy.get("[data-cy=fin]").type(fecha15.toISOString().slice(0, 10));
    cy.get("[data-cy=filtrar-boton]").click();

    const fecha16 = new Date(hoy);
    fecha16.setDate(hoy.getDate() - 30 * 6);
    const fecha17 = new Date(hoy);
    fecha17.setDate(hoy.getDate() - 1);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "semestral").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha16)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha17)).should("be.visible");
    cy.contains(".etiqueta-estado", "Finalizado").should("be.visible");

    // Varios filtros
    cy.get("[data-cy=select-tarifa]").select("");
    const fecha18 = new Date(hoy);
    fecha18.setDate(hoy.getDate() - 30 * 12);
    cy.get("[data-cy=inicio]").type(fecha18.toISOString().slice(0, 10));

    const fecha19 = new Date(hoy);
    fecha19.setDate(hoy.getDate() + 30 * 2 * 12);
    cy.get("[data-cy=fin]").type(fecha19.toISOString().slice(0, 10));
    cy.get("[data-cy=filtrar-boton]").click();

    const fecha20 = new Date(hoy);
    fecha20.setDate(hoy.getDate() - 30 * 6);
    const fecha21 = new Date(hoy);
    fecha.setDate(hoy.getDate() - 1);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa semestral").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha20)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha21)).should("be.visible");

    const fecha22 = new Date(hoy);
    fecha22.setDate(hoy.getDate() + 30 * 6);
    const fecha23 = new Date(hoy);
    fecha23.setDate(hoy.getDate() + 30 * 18 - 1);

    cy.contains(".lugar-nombre", "usuario2").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa anual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha22)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha23)).should("be.visible");
    cy.contains(".etiqueta-estado", "Pendiente de inicio").should("be.visible");

    const fecha24 = new Date(hoy);
    fecha24.setDate(hoy.getDate());
    const fecha25 = new Date(hoy);
    fecha25.setDate(hoy.getDate() + 29);

    cy.contains(".lugar-nombre", "usuario").should("be.visible");
    cy.contains(".lugar-tarifa", "Tarifa mensual").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha24)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha25)).should("be.visible");
    cy.contains(".etiqueta-estado", "Activo").should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_gestor']").click();
    cy.url().should("include", "/menu_gestor");

    // Actualizamos tarifas
    cy.get("[data-cy=act-tar-page]").click();
    cy.url().should("include", "/actualizar_tarifas");
    cy.wait(1000);

    // Seleccionamos tarifa anual
    cy.get("[data-cy='siguiente-tarifa']").click();
    cy.get("[data-cy='siguiente-tarifa']").click();

    cy.contains("Tarifa anual").should("be.visible");
    cy.contains("Duración: Anual").should("be.visible");
    cy.contains(
      "Descripción: Esta tarifa permite hacer un renovacion al año y olvidarte"
    ).should("be.visible");
    cy.contains("Importe: 10€").should("be.visible");
    cy.contains("Precio por minuto: 0.02€").should("be.visible");

    // Actualizamos importe y precio por minuto
    cy.get("[data-cy=n-imp]").type("5");
    cy.get("[data-cy=n-pm]").type("0.3");
    cy.get("[data-cy=act-tar]").click();

    // Volvemos al menú inicial y volvemos a acceder para ver si se ha actualizado
    cy.get("[data-cy='/menu_gestor']").click();
    cy.url().should("include", "/menu_gestor");

    cy.get("[data-cy=act-tar-page]").click();
    cy.url().should("include", "/actualizar_tarifas");

    cy.get("[data-cy='siguiente-tarifa']").click().click();
    cy.get("[data-cy='siguiente-tarifa']").click();

    cy.contains("Importe: 5€").should("be.visible");
    cy.contains("Precio por minuto: 0.3€").should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_gestor']").click();
    cy.url().should("include", "/menu_gestor");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");
  });
});
