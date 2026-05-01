// cypress/e2e/test_integracion_1.cy.js
describe("Test Integracion 1", () => {
  // Realiza las acciones de un nuevo usuario que desea utilizar el servicio:
  // - Consultar tarifas disponibles de la aplicación.
  // - Consulta el estado del campus para conocer las estaciones disponibles.
  // - Realiza el alta de usuario.
  // - Realiza su primer inicio de sesión.

  it("Acciones de un usuario interesado en el servicio", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    //Poblamos la base de datos con los datos iniciales necesarios
    cy.populate_inicial_cypress();

    // Página de inicio
    cy.visit("/");
    cy.wait(1000);
    // Consulta las tarifas existentes

    // Consultamos tarifa mensual y obtenemos su información
    cy.contains("Duración: Mensual").should("be.visible");
    cy.contains(
      "Descripción: Esta tarifa permite realizar un número de reservas ilimitadas a coste 0."
    ).should("be.visible");
    cy.contains("Importe: 30€").should("be.visible");
    cy.contains("Precio por minuto: 0€").should("be.visible");

    // Tarifa semestral
    cy.get("[data-cy=siguiente]").click();
    cy.contains("Duración: Semestral").should("be.visible");
    cy.contains(
      "Descripción: Esta tarifa permite realizar reservas con un coste bajo."
    ).should("be.visible");
    cy.contains("Importe: 10€").should("be.visible");
    cy.contains("Precio por minuto: 0.02€").should("be.visible");

    // Tarifa anual
    cy.get("[data-cy=siguiente]").click();
    cy.contains("Duración: Anual").should("be.visible");
    cy.contains(
      "Descripción: Esta tarifa permite hacer un renovacion al año y olvidarte"
    ).should("be.visible");
    cy.contains("Importe: 10€").should("be.visible");
    cy.contains("Precio por minuto: 0.02€").should("be.visible");

    // Consultamos el estado de cada estación
    // Vamos a la página de consultar estado
    cy.get("[data-cy='/consultar_estado']").click();
    cy.url().should("include", "/consultar_estado");
    cy.get("[data-cy=titulo-estado]").should("exist");
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

    // Volvemos al menú inicial
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Procede a darse de alta

    // Vamos a página de crear cuenta
    cy.get("[data-cy='/alta_usuario']").click();
    cy.url().should("include", "/alta_usuario");
    cy.get("[data-cy=alta-tit]").should("exist");

    cy.get("[data-cy=nombre]").type("Luis");
    cy.get("[data-cy=apellidos]").type("Gonzalez Gonzalez");
    cy.get("[data-cy=usuario]").type("cypress");
    cy.get("[data-cy=contraseña]").type("Contracypress26$");
    cy.get("[data-cy=tlf]").type("111222333");
    cy.get("[data-cy=select-tarifa-alta]").select("mensual");

    // Pulsa botón de alta
    cy.get("[data-cy=alta-button]").click();

    // Debe redirigirnos al pago
    cy.url().should("include", "/pago_alta");

    // Información de pago
    cy.contains("Información general de la factura").should("be.visible");
    cy.contains("Usuario: cypress").should("be.visible");
    cy.contains("Importe: 30€").should("be.visible");
    cy.contains("Finalización del contrato:").should("be.visible");
    const hoy = new Date();
    const fecha = new Date(hoy);
    fecha.setDate(hoy.getDate() + 29);
    const fechaFormateada = fecha.toISOString().slice(0, 10);
    cy.contains(fechaFormateada).should("be.visible");

    // Suponemos que el pago se realizó correctamente creando usuario
    cy.populate_integracion1();

    // Volvemos al menú inicial
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Iniciamos sesión con los datos del usuario creado
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("cypress");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos al menú inicial del usuario
    cy.url().should("include", "/menu_usuario");
  });
});
