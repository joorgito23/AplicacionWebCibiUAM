const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    specPattern: "cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}",
    baseUrl: "http://localhost:5173",
    viewportWidth: 1536,
    viewportHeight: 1024,
  },
  component: {
    specPattern: "src/**/__tests__/*.{cy,spec}.{js,ts,jsx,tsx}",
    devServer: {
      framework: "vue",
      bundler: "vite",
    },
  },

  env: {
    python: "/home/jorge/Documentos/TFG/env/bin/python",
    manage: "/home/jorge/Documentos/TFG/AplicacionWebCibiUAM/backend/manage.py",
  },
});
