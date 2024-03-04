import {GenezioDeploy} from "@genezio/types";

@GenezioDeploy()
export class CronExample {
    constructor() {
        this.counter = 0
    }

    sayHiEveryMinute() {
        this.counter += 1
    }

    getCounter() {
        return this.counter
    }
}
