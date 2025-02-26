import { defineConfig } from "cypress";
import process from "process";
import dotenv from "dotenv";

dotenv.config();

export default defineConfig({
  e2e: {
    experimentalRunAllSpecs: true,
    baseUrl: "<NEXT_URL>",
    setupNodeEvents(on, config) {
      on('before:browser:launch', (browser, launchOptions) => {
        if (browser.name === 'chrome' || browser.name === 'chromium') {
          launchOptions.args.push('--disable-gpu');
          launchOptions.args.push('--no-sandbox');
          launchOptions.args.push('--disable-dev-shm-usage');
        }
        return launchOptions;
      });
    },
    video: false,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false,
  },
  env: {
    url: "<NEXT_URL>",
  },
  retries: {
    runMode: 2,
    openMode: 0
  }
});
