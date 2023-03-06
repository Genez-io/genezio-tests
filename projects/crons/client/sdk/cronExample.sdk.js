/**
* This is an auto generated code. This code should not be modified since the file can be overwriten 
* if new genezio commands are executed.
*/
   
  import { Remote } from "./remote.js"
  
  export class CronExample {
      static remote = new Remote("http://127.0.0.1:32233/CronExample")
  
      static async getCounter() {
          return CronExample.remote.call("CronExample.getCounter")  
      }
      
      
  }
  
  export { Remote };
  