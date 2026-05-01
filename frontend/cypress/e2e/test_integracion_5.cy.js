// cypress/e2e/test_integracion_5.cy.js
describe("Test Integracion 5", () => {
  // Realiza las acciones de un usuario que desea realizar una reserva:
  // - Realiza login
  // - Consulta el estado del campus para conocer disponibilidad de estaciones
  // - Realiza una reserva para desplazarse
  // - Lee su notificación de reserva
  // - Consulta sus reservas para ver que todo está correcto
  // - Cierra sesión
  // - Otro usuario accede y realiza una reserva con coste

  it("Acciones de un usuario registrado", () => {
    // Borramos toda la base de datos inicial
    cy.reset_bd();

    // Poblamos base de datos con datos iniciales necesarios
    cy.populate_integracion5();

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

    // Debemos ser redirigidos a menú inicial
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
    cy.contains("Bicicletas disponibles: 1").should("be.visible");
    cy.contains("Anclajes libres: 2").should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Realizamos una reserva
    // Vamos a página de realizar reserva
    cy.get("[data-cy=reserva-page]").click();
    cy.url().should("include", "/realizar_reserva");

    // Rellenamos formulario de reserva
    const hoy = new Date().toISOString().split("T")[0];
    const ahora = new Date();

    // Hora Inicio
    const hInicio = new Date(ahora);
    hInicio.setMinutes(hInicio.getMinutes() + 30);

    // Hora Fin
    const hFin = new Date(ahora);
    hFin.setMinutes(hFin.getMinutes() + 40);

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

    // Mensaje de reserva realizada
    cy.get("[data-cy=msg]").should("exist");

    cy.wait(6000);

    // Debemos ser redirigidos a menú inicial
    cy.url().should("include", "/menu_usuario");

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
    const fecha1 = new Date(ahora);
    cy.contains(fecha1.toISOString().slice(0, 10)).should("be.visible");
    cy.contains("A continuación se indica un resumen de su reserva.").should(
      "be.visible"
    );

    // Notificación aviso expiración contrato
    const fecha2 = new Date(ahora);
    fecha2.setDate(fecha2.getDate() - 25 + 29 - 10);
    cy.contains(fecha2.toISOString().slice(0, 10)).should("be.visible");
    cy.contains(
      "Su contrato expira en 10 días. Debe renovar el contrato en caso de no haber realizado la renovación."
    ).should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Accedemos a nuestra sección de notificaciones para ver que no hay ninguna
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
    fecha3.setMinutes(fecha3.getMinutes() + 30);
    const fecha4 = new Date(ahora);
    fecha4.setMinutes(fecha4.getMinutes() + 40);
    cy.contains(".etiqueta-estado", "Pendiente").should("be.visible");
    cy.contains(".info-value", formatFecha(fecha3)).should("be.visible");
    cy.contains(".info-value", formatFecha(fecha4)).should("be.visible");

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");

    // Iniciamos sesión con los datos del otro usuario
    // Ir a página de login
    cy.get("[data-cy='/login']").click();

    // Rellena formulario
    cy.get("[data-cy=username]").type("usuario2");
    cy.get("[data-cy=password]").type("Contracypress26$");

    // Pulsa botón de login
    cy.get("[data-cy=login-button]").click();

    // Realizamos una reserva
    // Vamos a página de realizar reserva
    cy.get("[data-cy=reserva-page]").click();
    cy.url().should("include", "/realizar_reserva");

    // Rellenamos formulario de reserva

    // Hora Inicio
    hInicio.setMinutes(hInicio.getMinutes() + 30);

    // Hora Fin
    hFin.setMinutes(hFin.getMinutes() + 30);

    const horaInicio2 = `${String(hInicio.getHours()).padStart(
      2,
      "0"
    )}:${String(hInicio.getMinutes()).padStart(2, "0")}`;
    const horaFin2 = `${String(hFin.getHours()).padStart(2, "0")}:${String(
      hFin.getMinutes()
    ).padStart(2, "0")}`;

    cy.get("[data-cy=select-reserva-destino]").select(
      "Facultad de Formación de Profesorado y Educación"
    );
    cy.get("[data-cy=select-reserva-origen]").select("EPS");
    cy.get("[data-cy=fechaInicio]").type(hoy);
    cy.get("[data-cy=horaInicio]").type(horaInicio2);
    cy.get("[data-cy=fechaFin]").type(hoy);
    cy.get("[data-cy=horaFin]").type(horaFin2);
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
    cy.contains(horaInicio2).should("be.visible");
    cy.contains(horaFin2).should("be.visible");
    cy.contains("EPS").should("be.visible");
    cy.contains("Facultad de Formación de Profesorado y Educación").should(
      "be.visible"
    );

    // Volvemos al menú inicial
    cy.get("[data-cy='/menu_usuario']").click();
    cy.url().should("include", "/menu_usuario");

    // Hacemos logout
    cy.get("[data-cy='/']").click();
    cy.url().should("include", "/");
  });
});
