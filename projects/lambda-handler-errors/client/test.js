import { Server } from "@genezio-sdk/lambda-handler-errors_us-east-1"

(async () => {
  await Server.method().catch((error) => {
    console.log(error);
  })
})();
