import { defineConfig } from "cypress";
import process from "process";

export default defineConfig({
  e2e: {
    experimentalRunAllSpecs: true,
    baseUrl: process.env.NEXT_URL || 'http://localhost:3000',
    setupNodeEvents(on, config) {
    },
    video: false,
    screenshotOnRunFailure: true,
  },
  env: {
    url: process.env.NEXT_URL,
  },
  retries: {
    runMode: 2,
    openMode: 0
  }
});
