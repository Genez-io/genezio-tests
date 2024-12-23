import { TaskModel } from "./models/task"
import { UserModel } from "./models/user"
import { ActiveSession } from "./models/activeSession"
import { mongoose } from "mongoose"
import { MONGO_DB_URI } from "./helper"
import {GenezioDeploy, GenezioMethod} from "@genezio/types";

@GenezioDeploy()
export class Cron {
  constructor() {
    this.#connect();
  }

  /**
   * Private method used to connect to the DB.
   */
  #connect() {
    mongoose.connect(MONGO_DB_URI);
  }

  /**
   * Method that will be called by the cron job.
   *
   * The method will delete all the data from the DB.
   */
  @GenezioMethod({type: "cron", cronString: "0 12 * * *"})
  async deleteAllData() {
    console.log("Deleting all data from the DB");
    try {
      await TaskModel.deleteMany({});
      console.log("Tasks deleted");
    } catch (error) {
      console.log("Error deleting tasks", error);
    }

    try {
      await ActiveSession.deleteMany({});
      console.log("Active sessions deleted");
    } catch (error) {
      console.log("Error deleting active sessions", error);
    }

    try {
      await UserModel.deleteMany({});
      console.log("Users deleted");
    } catch (error) {
      console.log("Error deleting users", error);
    }

  }
}
