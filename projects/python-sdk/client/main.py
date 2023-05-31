from sdk.server import Server

serverTest = Server()

print(serverTest.method(), end="")
print(serverTest.methodWithMultipleParameters("123", 2.0), end="")
print(serverTest.methodWithOneParameter("123"), end="")
print(serverTest.methodWithoutParameters(), end="")