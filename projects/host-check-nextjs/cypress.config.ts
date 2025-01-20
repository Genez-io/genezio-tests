import { defineConfig } from "cypress";
import process from "process";

export default defineConfig({
  e2e: {
    experimentalRunAllSpecs: true,
    baseUrl: process.env.NEXT_URL || 'http://localhost:3000',
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
    url: process.env.NEXT_URL,
  },
  retries: {
    runMode: 2,
    openMode: 0
  }
});
