const {Server} = require("@genezio-sdk/lambda-handler-errors");

(async () => {
  await Server.method().catch((error) => {
    console.log(error);
  })
})();
