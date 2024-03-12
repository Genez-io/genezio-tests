const { CronExample } = require("@genezio-sdk/cron-example-runtime");
/**
 * Client that makes requests to the HelloWorldService deployed on genezio.
 * 
 * Before running this script, run either "genezio deploy" or "genezio local".
 */

(async () => {
    // Use the SDK to make requests to the Hello World Service.
    console.log(await CronExample.getCounter())
})();
