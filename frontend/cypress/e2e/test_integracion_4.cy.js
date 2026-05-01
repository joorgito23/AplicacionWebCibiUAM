// cypress/e2e/test_integracion_4.cy.js
describe("Test Integracion 4", () => {
  // Realiza las acciones cotidianas de un administrador que desea gestionar los gestores del sistema:
  // - Realiza login
  // - Crea un nuevo gestor contratado
  // - Da de baja a un gestor
  // - Realiza logout

  it("Acciones de un administrador registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    //Poblamos base de datos con datos iniciales necesarios
    cy.populate_integracion4();

    // Página inicio
    cy.visit("/");

    // Iniciamos sesión con los datos del administrador
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("admin");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_admin");

    // Comprobamos que muestra todas las opciones de funcionalidad del administrador
    cy.contains("¿Qué acción desea realizar como administrador?").should(
      "be.visible"
    );
    cy.contains("Alta de Gestor").should("be.visible");
    cy.contains("Baja de Gestor").should("be.visible");

    // Damos de alta un gestor

    // Rellena formulario
    cy.get("[data-cy=nombre]").type("Juan");
    cy.get("[data-cy=apellidos]").type("Gonzalez Gonzalez");
    cy.get("[data-cy=usuario]").type("gestorCreado");
    cy.get("[data-cy=contraseña]").type("Contracypress26$");

    // Pulsa botón de alta
    cy.get("[data-cy=alta-gest]").click();
    cy.get("[data-cy=msg]").should("exist");
    cy.wait(6000);

    // Damos de baja un gestor creado
    // Consultamos que muestra todos los gestores
    cy.get("td").contains("gestorPrueba").should("be.visible");
    cy.get("td").contains("luis").should("be.visible");
    cy.get("td").contains("perez").should("be.visible");
    cy.get("td").contains("gestorCreado").should("be.visible");
    cy.get("td").contains("Juan").should("be.visible");
    cy.get("td").contains("Gonzalez Gonzalez").should("be.visible");

    // Seleccionamos gestor y pulsamos el botón eliminar
    cy.get("[data-cy=boton-gestorPrueba]").click();
    cy.get("[data-cy=confirmarBaja]").click();

    // Comprobamos que no está el gestor borrado
    cy.get("td").contains("gestorPrueba").should("not.exist");
    cy.get("td").contains("luis").should("not.exist");
    cy.get("td").contains("perez").should("not.exist");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Autenticamos al gestor creado para ver que puede acceder

    // Iniciamos sesión con los datos del gestor
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("gestorCreado");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_gestor");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Tratamos de acceder con el gestor borrado
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("gestorPrueba");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Mensaje error acceso
    cy.get("[data-cy=error]").should("exist");

    cy.url().should("include", "/");
    cy.url().should("not.include", "/menu_gestor");
  });
});
