import { HelloWorldService } from "./sdk/helloWorldService.sdk.js"

console.log(await HelloWorldService.methodWithReturnSimpleString("George"))
console.log(await HelloWorldService.getPoints(1, 2, 3))