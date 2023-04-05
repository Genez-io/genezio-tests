# This is an auto generated code. This code should not be modified since the file can be overwriten 
# if new genezio commands are executed.
   
from .remote import Remote

class Server:
    remote = Remote("http://127.0.0.1:4422/Server")

    def method():
        return Server.remote.call("Server.method")  
      
    def methodWithoutParameters():
        return Server.remote.call("Server.methodWithoutParameters")  
      
    def methodWithOneParameter(test1):
        return Server.remote.call("Server.methodWithOneParameter", test1)  
  
    def methodWithMultipleParameters(test1, test2):
        return Server.remote.call("Server.methodWithMultipleParameters", test1, test2)  
  
    

