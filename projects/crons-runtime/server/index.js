import {GenezioDeploy, GenezioMethod} from "@genezio/types";

@GenezioDeploy()
export class CronExample {
    constructor() {
        this.counter = 0
    }

    @GenezioMethod({type:"cron",cronString:"* * * * *"})
    sayHiEveryMinute() {
        this.counter += 1
    }

    getCounter() {
        return this.counter
    }
}
