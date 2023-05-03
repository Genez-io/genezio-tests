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

  final arrayResponse = await HelloWorldService.getNumbers(1, 2, 3);
  stdout.write('${arrayResponse.length} ${arrayResponse[0]} ${arrayResponse[1]} ${arrayResponse[2]}');

  final stringsArrayResponse = await HelloWorldService.getStrings("1", "2", "3");
  stdout.write('${stringsArrayResponse.length} ${stringsArrayResponse[0]} ${stringsArrayResponse[1]} ${stringsArrayResponse[2]}');

  final futureStringsArrayResponse = await HelloWorldService.getNumbersAsFuture(1, 2, 3);
  stdout.write('${futureStringsArrayResponse.length} ${futureStringsArrayResponse[0]} ${futureStringsArrayResponse[1]} ${futureStringsArrayResponse[2]}');

  final pointResponse = await HelloWorldService.getPoints(1, 2, 3);
  stdout.write('${pointResponse.length} ${pointResponse[0].x} ${pointResponse[0].y} ${pointResponse[1].x} ${pointResponse[1].y} ${pointResponse[2].x} ${pointResponse[2].y}');

  
  final pointAsyncResponse = await HelloWorldService.getPointsAsync(1, 2, 3);
  stdout.write('${pointAsyncResponse.length} ${pointAsyncResponse[0].x} ${pointAsyncResponse[0].y} ${pointAsyncResponse[1].x} ${pointAsyncResponse[1].y} ${pointAsyncResponse[2].x} ${pointAsyncResponse[2].y}');

  final replacedPoints = await HelloWorldService.replacePointsInArray([Point(1, 2), Point(3, 4), Point(5, 6)]);
  stdout.write('${replacedPoints.length} ${replacedPoints[0].x} ${replacedPoints[0].y} ${replacedPoints[1].x} ${replacedPoints[1].y} ${replacedPoints[2].x} ${replacedPoints[2].y}');

  final replacedPointsInMap = await HelloWorldService.replacePointsInMap({"hello": Point(1, 2)});
  stdout.write('${replacedPointsInMap.length} ${replacedPointsInMap["hello"]!.x} ${replacedPointsInMap["hello"]!.y}');
}