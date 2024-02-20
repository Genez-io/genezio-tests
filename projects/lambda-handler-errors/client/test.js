import {Server} from "./sdk/server.sdk.js"

(async () => {
  await Server.method().catch((error) => {
    console.log(error);
  })
})();
