import { BinaryDependencyTest } from "@genezio-sdk/binary-dependency-runtime"

(async () => {
    const result = await BinaryDependencyTest.test()
    const regexExp = /^[$0-9a-zA-Z.\/]*$/gi;
    const correct = regexExp.test(result);

    console.log(correct ? "Ok" : "Error")
})();