import 'package:json_annotation/json_annotation.dart';
part 'server.g.dart';

@JsonSerializable()
class Point {
  int x;
  int y;

  factory Point.fromJson(Map<String, dynamic> json) => _$PointFromJson(json);

  Map<String, dynamic> toJson() => _$PointToJson(this);

  Point(this.x, this.y);
}

@JsonSerializable()
class TestResult {
  int number;
  String string;
  Point point;

  TestResult(this.number, this.string, this.point);

  factory TestResult.fromJson(Map<String, dynamic> json) =>
      _$TestResultFromJson(json);

  Map<String, dynamic> toJson() => _$TestResultToJson(this);
}

class HelloWorldService {
  var methodWithVoidReturnVoidCount = 0;
  var methodWithStringReturnVoidParam = "";
  var methodWithPointReturnVoidParam = Point(0, 0);

  void methodWithVoidReturnVoid() {
    methodWithVoidReturnVoidCount = 100;
  }

  void methodWithStringReturnVoid(String string) {
    this.methodWithStringReturnVoidParam = string;
  }

  void methodWithPointReturnVoid(Point point) {
    this.methodWithPointReturnVoidParam = point;
  }

  String methodWithReturnSimpleString() {
    return "hello";
  }

  int methodWithReturnSimpleInt() {
    return 42;
  }

  bool methodWithReturnSimpleBool() {
    return true;
  }

  List<Point> replacePointsInArray(List<Point> list) {
    return [Point(list[0].x + 10, list[0].y + 10), Point(list[1].x + 10, list[1].y + 10), Point(list[2].x + 10, list[2].y + 10)];
  }

  List<int> getNumbers(int x, int y, int z) {
    return [x, y, z];
  }

  List<String> getStrings(String x, String y, String z) {
    return [x, y, z];
  }

  Future<List<int>> getNumbersAsFuture(int x, int y, int z) {
    return Future.value([x, y, z]);
  }

  List<Point> getPoints(int x, int y, int count) {
    return List.generate(count, (index) => Point(x * index, y * index));
  }

  Future<List<Point>> getPointsAsync(int x, int y, int count) {
    return Future.value(List.generate(count, (index) => Point(x * index, y * index)));
  }

  TestResult getTestResult() {
    return TestResult(
        this.methodWithVoidReturnVoidCount,
        this.methodWithStringReturnVoidParam,
        this.methodWithPointReturnVoidParam);
  }
}
