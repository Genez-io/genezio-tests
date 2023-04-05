/**
* This is an auto generated code. This code should not be modified since the file can be overwriten 
* if new genezio commands are executed.
*/
   
  import { Remote } from "./remote.js"
  
  export class Server {
      static remote = new Remote("http://127.0.0.1:37870/Server")
  
      static async method() {
          return Server.remote.call("Server.method")  
      }
      
      static async methodWithoutParameters() {
          return Server.remote.call("Server.methodWithoutParameters")  
      }
      
      static async methodWithOneParameter(test1) {
          return Server.remote.call("Server.methodWithOneParameter", test1)  
      }
  
      static async methodWithMultipleParameters(test1, test2) {
          return Server.remote.call("Server.methodWithMultipleParameters", test1, test2)  
      }
  
      
  }
  
  export { Remote };
  