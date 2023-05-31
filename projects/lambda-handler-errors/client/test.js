import {Server} from "./sdk/server.sdk.js"

(async () => {
  
  const res = await Server.method();
  console.log(res === "Error: Error from server" ? "Ok" : "Error");
})();
