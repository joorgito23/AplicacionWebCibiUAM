// Comandos usados en los test para borrar y poblar la base de datos

Cypress.Commands.add("reset_bd", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/reset.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_inicial_cypress", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion1", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy1.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion2", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy2.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion2_1", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy2_1.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion3", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy3.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion4", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy4.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion5", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy5.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion6", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy6.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion6_1", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy6_1.py";

  cy.exec(`${python} ${path}`);
});

Cypress.Commands.add("populate_integracion7", () => {
  const python = Cypress.env("python");
  const path = "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/populate_cy7.py";

  cy.exec(`${python} ${path}`);
});
