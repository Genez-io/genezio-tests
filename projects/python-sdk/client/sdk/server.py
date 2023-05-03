# This is an auto generated code. This code should not be modified since the file can be overwriten 
# if new genezio commands are executed.
  
from .remote import Remote
from typing import Any, List
from enum import IntEnum
from collections.abc import Mapping


class Server:
  remote = Remote("http://127.0.0.1:8083/Server")

  def method(self) -> Any:
    return Server.remote.call("Server.method")

  def methodWithoutParameters(self) -> str:
    return Server.remote.call("Server.methodWithoutParameters")

  def methodWithOneParameter(self, test1: str) -> str:
    return Server.remote.call("Server.methodWithOneParameter", test1)

  def methodWithMultipleParameters(self, test1: str, test2: float) -> str:
    return Server.remote.call("Server.methodWithMultipleParameters", test1, test2)

