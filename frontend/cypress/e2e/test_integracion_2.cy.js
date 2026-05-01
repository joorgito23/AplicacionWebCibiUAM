// cypress/e2e/test_integracion_2.cy.js
describe("Test Integracion 2", () => {
  // Realiza las acciones de un usuario que desea utilizar la aplicación:
  // - Realiza login
  // - Consulta el estado actual del campus
  // - Consulta su perfil
  // - Actualiza su número de teléfono
  // - Actualiza contraseña
  // - Lee las notificaciones que tiene pendientes de lectura
  // - Renueva su contrato tras ser informado en una notificación que le quedan menos de 10 días
  // - Realiza logout

  it("Acciones de un usuario registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    // Poblamos base de datos con datos iniciales necesarios
    cy.populate_integracion2();

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

    // Consultamos estado
    // Vamos a página de consultar estado
    cy.get("[data-cy='estado-page']").click();
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
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Consultamos nuestro perfil
    // Vamos a página de consultar perfil
    cy.get("[data-cy='/consultar_perfil']").click();
    cy.url().should("include", "/consultar_perfil");

    // Comprobamos que muestra la información correcta
    cy.get("[data-cy=titulo-perfil]").should("exist");
    cy.contains("Nombre de Usuario: usuario").should("be.visible");
    cy.contains("Nombre y Apellidos: Luis Perez Perez").should("be.visible");
    cy.contains("Rol: usuario").should("be.visible");
    cy.contains("Tarifa Actual: Mensual").should("be.visible");
    cy.contains("Contraseña Actual:").should("be.visible");
    cy.contains("Nueva Contraseña:").should("be.visible");
    cy.contains("Repita Nueva Contraseña:").should("be.visible");

    const hoy = new Date();
    const fecha = new Date(hoy);
    fecha.setDate(hoy.getDate() - 25 + 29);
    cy.contains(fecha.toISOString().slice(0, 10)).should("be.visible");
    cy.contains("Saldo Disponible: 0€").should("be.visible");
    cy.contains("Teléfono:").should("be.visible");
    cy.get("[data-cy=input-tlf]").invoke("val").should("equal", "111111111");

    // Actualiza su número de teléfono
    cy.get("[data-cy=input-tlf]").clear().type("222222222");
    cy.get("[data-cy=act-tlf]").click();

    // Actualiza su contraseña
    cy.get("[data-cy=input-pass-antigua]").clear().type("Contracypress26$");
    cy.get("[data-cy=input-pass-nueva]").clear().type("Contracypress261$");
    cy.get("[data-cy=input-pass-nueva2]").clear().type("Contracypress261$");
    cy.get("[data-cy=act-pass]").click();

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Volvemos a consultar nuestro perfil para ver que se ha actualizado el teléfono
    cy.get("[data-cy='/consultar_perfil']").click();
    cy.url().should("include", "/consultar_perfil");
    cy.contains("Teléfono:").should("be.visible");
    cy.get("[data-cy=input-tlf]").invoke("val").should("equal", "222222222");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Hacemos login con la nueva contraseña
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("usuario");
    cy.get("[data-cy=password]").type("Contracypress261$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Accedemos a nuestra sección de notificaciones
    cy.get("[data-cy='/leer_notificaciones']").click();
    cy.url().should("include", "/leer_notificaciones");

    // Verificamos que muestra las notificaciones que debe tener el usuario
    cy.contains("Notificaciones de usuario").should("be.visible");
    cy.contains(
      "No dispones de notificaciones pendientes de lectura actualmente."
    ).should("not.exist");
    cy.contains("Notificaciones sin leer").should("be.visible");
    cy.contains("Fecha:").should("be.visible");

    // Notificación 1
    const fecha1 = new Date(hoy);
    fecha1.setDate(hoy.getDate() - 12 * 30);
    cy.contains(fecha1.toISOString().slice(0, 10)).should("be.visible");
    cy.contains("Prueba 1").should("be.visible");

    // Notificación 2
    const fecha2 = new Date(hoy);
    fecha2.setDate(hoy.getDate() - 30);
    cy.contains(fecha2.toISOString().slice(0, 10)).should("be.visible");
    cy.contains("Prueba 2").should("be.visible");

    // Notificación de aviso de expiración contrato
    const fecha3 = new Date(hoy);
    fecha3.setDate(hoy.getDate() - 25 + 29 - 10);
    cy.contains(fecha3.toISOString().slice(0, 10)).should("be.visible");
    cy.contains(
      "Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación."
    ).should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Accedemos a nuestra sección de notificaciones para ver que no hay ninguna tras haber leído todas
    cy.get("[data-cy='/leer_notificaciones']").click();
    cy.url().should("include", "/leer_notificaciones");

    cy.contains("Notificaciones de usuario").should("be.visible");
    cy.contains(
      "No dispones de notificaciones pendientes de lectura actualmente."
    ).should("be.visible");
    cy.contains("Notificaciones sin leer").should("not.exist");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Accedemos a la sección de renovación de contrato
    cy.get("[data-cy='renovar-page']").click();
    cy.url().should("include", "/renovar_contrato");

    // Verificamos que muestra la información para renovar el contrato
    cy.contains("Renovar Contrato").should("be.visible");

    // Comprobamos que nos permite seleccionar las tarifas existentes
    cy.get("[data-cy=select-tarifa]")
      .contains("option", "-- Seleccione --")
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

    // Seleccionamos anual
    cy.get("[data-cy=select-tarifa]").select("anual");
    cy.get("[data-cy=renovar-boton]").click();

    // Debemos ser redirigidos a la pantalla de pago
    cy.url().should("include", "/pagar_renovacion");

    // Verificamos que muestra la información del pago
    cy.contains("Pago de la Renovación del Contrato").should("be.visible");
    cy.contains("Información general de la factura").should("be.visible");
    cy.contains("Usuario: usuario").should("be.visible");
    cy.contains("Importe: 10€").should("be.visible");
    cy.contains("Finalización del contrato:").should("be.visible");
    const fecha4 = new Date(hoy);
    fecha4.setDate(hoy.getDate() - 25 + 30 + 12 * 30 - 1);
    cy.contains(fecha4.toISOString().slice(0, 10)).should("be.visible");

    // Suponemos que el pago se realizó correctamente renovando contrato
    cy.populate_integracion2_1();

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");
  });
});
