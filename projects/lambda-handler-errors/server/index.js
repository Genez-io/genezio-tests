import {GenezioDeploy} from "@genezio/types";

@GenezioDeploy()
export class Server {
  method() {
    throw new Error('Error from server');
  }
}