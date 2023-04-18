/**
* This is an auto generated code. This code should not be modified since the file can be overwriten
* if new genezio commands are executed.
*/

import { Remote } from "./remote.js"

export class BinaryDependencyTest {
  static remote = new Remote("https://bvvzjbdtuy4zzwfwojq5xdjpby0nrvrk.lambda-url.us-east-1.on.aws/")

  static async test() {
    return BinaryDependencyTest.remote.call("BinaryDependencyTest.test")
  }

}
