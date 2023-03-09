/**
* This is an auto generated code. This code should not be modified since the file can be overwriten 
* if new genezio commands are executed.
*/
     
import { Remote } from "./remote"

export type CreateUserResponse = {
  success: boolean,
  msg?: string
};

export type User = {
  _id: string,
  name: string,
  email: string,
};

export type UserLoginResponse = {
  success: boolean,
  user?: User,
  token?: string,
  msg?: string,
};

export type CheckSessionResponse = {
  success: boolean,
};



export class UserService {
    static remote = new Remote("https://jmuszpohoa5zrl6pqxmilfk4qa0xzorj.lambda-url.us-east-1.on.aws/")

    static async register(name: string, email: string, password: string): Promise<CreateUserResponse> {
        return await UserService.remote.call("UserService.register", name, email, password)  
  }

  static async login(email: string, password: string): Promise<UserLoginResponse> {
        return await UserService.remote.call("UserService.login", email, password)  
  }

  static async checkSession(token: string): Promise<CheckSessionResponse> {
        return await UserService.remote.call("UserService.checkSession", token)  
  }

  

}

export { Remote };
