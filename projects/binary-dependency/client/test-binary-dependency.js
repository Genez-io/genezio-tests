import { BinaryDependencyTest } from "./sdk/binaryDependencyTest.sdk.js"

(async () => {
    const result = await BinaryDependencyTest.test()
    const regexExp = /^[$0-9a-zA-Z.\/]*$/gi;
    const correct = regexExp.test(result);

    console.log(correct ? "Ok" : "Error")
})();