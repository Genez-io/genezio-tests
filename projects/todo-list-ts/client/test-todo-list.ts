import { UserService } from "./sdk/userService.sdk"
import { TaskService } from "./sdk/taskService.sdk"

/**
 * Client that makes requests to the HelloWorldService deployed on genezio.
 * 
 * Before running this script, run either "genezio deploy" or "genezio local".
 */

(async () => {
    const email = "test"+ Math.random()
    const result = await UserService.register("test", email, "test")
    console.log(result.success ? "Ok" : "Error");

    const loginResult = await UserService.login(email, "test")
    console.log(result.success ? "Ok" : "Error");

    const checkSessionResult = await UserService.checkSession(loginResult.token!)
    console.log(checkSessionResult.success ? "Ok" : "Error");

    const getAllTasksResult = await TaskService.getAllTasksByUser(loginResult.token!, loginResult.user!._id)
    console.log(getAllTasksResult.success ? "Ok" : "Error");
    console.log(getAllTasksResult.tasks.length === 0 ? "Ok" : "Error");

    const createTaskResult = await TaskService.createTask(loginResult.token!, "test", loginResult.user!._id)
    console.log(createTaskResult.success ? "Ok" : "Error");

    const getAllTasks2Result = await TaskService.getAllTasksByUser(loginResult.token!, loginResult.user!._id)
    console.log(getAllTasks2Result.success ? "Ok" : "Error");
    console.log(getAllTasks2Result.tasks.length === 1 ? "Ok" : "Error");
})();
