enum Season {
    SPRING,
    SUMMER,
    AUTUMN,
    WINTER
}

export type Model = {
    name: string
    type: string
    age: number
    season: Season
}

export type SuperModel = {
    id: string
    model: Model
}

export class ServerTest {
    async test(): Promise<string> {
        return "Hello from server!";
    }

    async test2(a: number): Promise<string> {
        return  a + "string"
    }

    async test3(a: Model): Promise<Model> {
        return {
            name: a.name,
            type: a.type,
            age: a.age + 1,
            season: Season.SPRING
        }
    }

    async test4(a: SuperModel): Promise<boolean> {
        if (a.model.age > 10) {
            return false
        } else {
            return true
        }
    }

    test5(a: number): number {
        return a + 1
    }

    async test6(n1: number, n2: number): Promise<number[]> {
        return [n1, n2]
    }

    // TODO: currently buggy
    // async test7() {
    //     console.log("test")
    // }

    // TODO: not currently supported
    // async test8(a: { [id: string]: number; }): Promise<{ [id: string]: number; }> {
    //     return {
    //         a: 2,
    //         b: 3,
    //     }
    // }

    test9(a: Season): Season {
        return a;
    }
}