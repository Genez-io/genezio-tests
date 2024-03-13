const {User} = require("@genezio-sdk/todo-list-runtime");
const {Task} = require("@genezio-sdk/todo-list-runtime");

/**
 * Client that makes requests to the HelloWorldService deployed on genezio.
 * 
 * Before running this script, run either "genezio deploy" or "genezio local".
 */

(async () => {
    const email = "test"+ Math.random()
    const result = await User.register("test", email, "test")
    console.log(result.success ? "Ok" : "Error");

    const loginResult = await User.login(email, "test")
    console.log(result.success ? "Ok" : "Error");

    const checkSessionResult = await User.checkSession(loginResult.token)
    console.log(checkSessionResult.success ? "Ok" : "Error");

    const getAllTasksResult = await Task.getAllTasksByUser(loginResult.token, loginResult.user._id)
    console.log(getAllTasksResult.success ? "Ok" : "Error");
    console.log(getAllTasksResult.tasks.length === 0 ? "Ok" : "Error");

    const createTaskResult = await Task.createTask(loginResult.token, "test", loginResult.user._id)
    console.log(createTaskResult.success ? "Ok" : "Error");

    const getAllTasks2Result = await Task.getAllTasksByUser(loginResult.token, loginResult.user._id)
    console.log(getAllTasks2Result.success ? "Ok" : "Error");
    console.log(getAllTasks2Result.tasks.length === 1 ? "Ok" : "Error");
})();
