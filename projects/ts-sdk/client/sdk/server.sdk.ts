/**
* This is an auto generated code. This code should not be modified since the file can be overwriten 
* if new genezio commands are executed.
*/
     
import { Remote } from "./remote"



export class Server {
    static remote = new Remote("http://127.0.0.1:18017/Server")

    static async method(): Promise<any> {
        return await Server.remote.call("Server.method")  
  }

  static async methodWithoutParameters(): Promise<string> {
        return await Server.remote.call("Server.methodWithoutParameters")  
  }

  static async methodWithOneParameter(test1: string): Promise<string> {
        return await Server.remote.call("Server.methodWithOneParameter", test1)  
  }

  static async methodWithMultipleParameters(test1: string, test2: number): Promise<string> {
        return await Server.remote.call("Server.methodWithMultipleParameters", test1, test2)  
  }

  

}

export { Remote };
