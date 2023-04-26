from sdk.serverTest import ServerTest, Model, SuperModel, Season

serverTest = ServerTest()

print(serverTest.test(), end="")
print(serverTest.test2(1.0), end="")
result = serverTest.test3(Model("name", "type", 1.0, Season.AUTUMN))
print(str(result.age)+str(result.name)+str(result.season)+str(result.type), end="")
print(serverTest.test4(SuperModel("id", Model("name", "type", 1.0, Season.AUTUMN))), end="")
print(serverTest.test4(SuperModel("id", Model("name", "type", 11, Season.AUTUMN))), end="")
print(serverTest.test5(21), end="")
print(serverTest.test6(11, 22), end="")
# print(serverTest.test7())
# print(serverTest.test8(1))
# print(serverTest.test9(Season.AUTUMN))
