import { defineConfig } from "cypress";
import process from "process";

export default defineConfig({
  e2e: {
    experimentalRunAllSpecs: true,
    setupNodeEvents(on, config) {
    },
  },
  env: {
    url: process.env.NEXT_URL,
  }
});
