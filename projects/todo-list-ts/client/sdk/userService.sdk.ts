/**
* This is an auto generated code. This code should not be modified since the file can be overwriten
* if new genezio commands are executed.
*/

import { Remote } from "./remote";

export type Task = {_id: string, title: string, ownerId: string, solved: boolean, date: Date};
export type GetTasksResponse = {success: boolean, tasks: Array<Task>};
export type GetTaskResponse = {success: boolean, task?: Task};
export type UpdateTaskResponse = {success: boolean};
export type DeleteTaskResponse = {success: boolean};
export type CreateUserResponse = {success: boolean, msg?: string};
export type User = {_id: string, name: string, email: string};
export type UserLoginResponse = {success: boolean, user?: User, token?: string, msg?: string};
export type CheckSessionResponse = {success: boolean};

export class UserService {
  static remote = new Remote("http://127.0.0.1:8083/UserService");

  static async register(name: string, email: string, password: string): Promise<CreateUserResponse> {
    return await UserService.remote.call("UserService.register", name, email, password);
  }
  static async login(email: string, password: string): Promise<UserLoginResponse> {
    return await UserService.remote.call("UserService.login", email, password);
  }
  static async checkSession(token: string): Promise<CheckSessionResponse> {
    return await UserService.remote.call("UserService.checkSession", token);
  }
}

export { Remote };
