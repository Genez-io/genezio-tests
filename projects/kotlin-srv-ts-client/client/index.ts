import {HelloWorldService} from "./sdk/helloWorldService.sdk"

async function main() {
  console.log(await HelloWorldService.methodWithReturnSimpleString("George"))
  console.log(await HelloWorldService.getPoints(1,2,3))
}

main()