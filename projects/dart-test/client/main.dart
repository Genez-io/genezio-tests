import "sdk/hello_world_service.dart";
import 'dart:io';

void main(List<String> args) async {
  await HelloWorldService.methodWithVoidReturnVoid();
  await HelloWorldService.methodWithStringReturnVoid("Hello World");
  await HelloWorldService.methodWithPointReturnVoid(Point(1, 2));
  final testResult = await HelloWorldService.getTestResult();
  stdout.write(testResult.number);
  stdout.write(testResult.string);
  stdout.write(testResult.point.x);
  stdout.write(testResult.point.y);

  final result = await HelloWorldService.getComplicatedClass(1, 2);
  stdout.write('${result.a.x} ${result.a.y}');
  stdout.write('${result.b.x} ${result.b.y}');
  result.otherPoints.forEach((element) {
    stdout.write('${element.x} ${element.y}');
  });

  result.pointsMap.forEach((key, value) {
    stdout.write(key);
    value.forEach((element) {
      stdout.write('${element.x} ${element.y}');
    });
  });

  result.pointsMap2.forEach((element) {
    element.forEach((element) {
      element.forEach((key, value) {
        stdout.write(key);
        value.forEach((element) {
          stdout.write('${element.x} ${element.y}');
        });
      });
    });
  });
}