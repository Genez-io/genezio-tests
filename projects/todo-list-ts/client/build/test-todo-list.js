"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const todo_list_ts_1 = require("@genezio-sdk/todo-list-ts");
const todo_list_ts_2 = require("@genezio-sdk/todo-list-ts");
/**
 * Client that makes requests to the HelloWorldService deployed on genezio.
 *
 * Before running this script, run either "genezio deploy" or "genezio local".
 */
(() => __awaiter(void 0, void 0, void 0, function* () {
    const email = "test" + Math.random();
    const result = yield todo_list_ts_1.UserService.register("test", email, "test");
    console.log(result.success ? "Ok" : "Error");
    const loginResult = yield todo_list_ts_1.UserService.login(email, "test");
    console.log(result.success ? "Ok" : "Error");
    const checkSessionResult = yield todo_list_ts_1.UserService.checkSession(loginResult.token);
    console.log(checkSessionResult.success ? "Ok" : "Error");
    const getAllTasksResult = yield todo_list_ts_2.TaskService.getAllTasksByUser(loginResult.token, loginResult.user._id);
    console.log(getAllTasksResult.success ? "Ok" : "Error");
    console.log(getAllTasksResult.tasks.length === 0 ? "Ok" : "Error");
    const createTaskResult = yield todo_list_ts_2.TaskService.createTask(loginResult.token, "test", loginResult.user._id);
    console.log(createTaskResult.success ? "Ok" : "Error");
    const getAllTasks2Result = yield todo_list_ts_2.TaskService.getAllTasksByUser(loginResult.token, loginResult.user._id);
    console.log(getAllTasks2Result.success ? "Ok" : "Error");
    console.log(getAllTasks2Result.tasks.length === 1 ? "Ok" : "Error");
}))();
