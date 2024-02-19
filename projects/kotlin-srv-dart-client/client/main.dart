import './sdk/hello_world_service.dart';

void main() async {
  print(await HelloWorldService.methodWithReturnSimpleString("test"));
  print(await HelloWorldService.methodWithReturnSimpleInt(1));
  print(await HelloWorldService.methodWithReturnSimpleBool());
  print(await HelloWorldService.getPoints(1,2,3));
}