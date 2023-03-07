/**
* This is an auto generated code. This code should not be modified since the file can be overwriten 
* if new genezio commands are executed.
*/
   
  import { Remote } from "./remote.js"
  
  export class BinaryDependencyTest {
      static remote = new Remote("http://127.0.0.1:8429/BinaryDependencyTest")
  
      static async test() {
          return BinaryDependencyTest.remote.call("BinaryDependencyTest.test")  
      }
      
      
  }
  
  export { Remote };
  