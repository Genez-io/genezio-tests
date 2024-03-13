from sdk.helloWorldService import HelloWorldService


def main():
    helloWorldService = HelloWorldService()
    helloWorldService.methodWithVoidReturnVoid()
    helloWorldService.methodWithStringReturnVoid("string")
    helloWorldService.methodWithPointReturnVoid({"x": 1, "y": 2})

    test_result = helloWorldService.getTestResult()
    print(test_result.number, end="")
    print(test_result.string, end="")
    print(test_result.point.x, end="")
    print(test_result.point.y, end="")

    string_return = helloWorldService.methodWithReturnSimpleString()
    int_return = helloWorldService.methodWithReturnSimpleInt()
    bool_return = helloWorldService.methodWithReturnSimpleBool()
    print(string_return, end="")
    print(int_return, end="")
    print(bool_return, end="")

    array_response = helloWorldService.getNumbers(1, 2, 3)
    print(array_response, end="")
    string_array_response = helloWorldService.getStrings("string1", "string2", "string3")
    print(string_array_response, end="")
    future_array_response = helloWorldService.getNumbersAsFuture(1, 2, 3)
    print(future_array_response, end="")
    points_response = helloWorldService.getPoints(1, 2, 3)
    print(points_response, end="")
    points_async_response = helloWorldService.getPointsAsync(1, 2, 3)
    print(points_async_response, end="")

    replaced_points = helloWorldService.replacePointsInArray([{"x": 1, "y": 2}, {"x": 3, "y": 4}, {"x": 5, "y": 6}])
    print(replaced_points, end="")


if __name__ == "__main__":
    main()
