import 'package:json_annotation/json_annotation.dart';
part 'hello_world.g.dart';

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

@JsonSerializable()
class ComplicatedClass {
  Point a;
  Point b;
  List<Point> otherPoints;
  Map<String, List<Point>> pointsMap;
  List<List<Map<String, List<Point>>>> pointsMap2;

  ComplicatedClass(
      this.a, this.b, this.otherPoints, this.pointsMap, this.pointsMap2);

  factory ComplicatedClass.fromJson(Map<String, dynamic> json) =>
      _$ComplicatedClassFromJson(json);

  Map<String, dynamic> toJson() => _$ComplicatedClassToJson(this);
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

  // TODO: we currently don't support this 
  List<int> getNumbers(int x, int y, int z) {
    return [x, y, z];
  }

  // TODO: we currently don't support this
  List<String> getStrings(String x, String y, String z) {
    return [x, y, z];
  }

  // TODO: we currently don't support this
  Future<List<int>> getNumbersAsFuture(int x, int y, int z) {
    return Future.value([x, y, z]);
  }

  TestResult getTestResult() {
    return TestResult(
        this.methodWithVoidReturnVoidCount,
        this.methodWithStringReturnVoidParam,
        this.methodWithPointReturnVoidParam);
  }

  ComplicatedClass getComplicatedClass(int x, int y) {
    return ComplicatedClass(Point(x, y), Point(x, y), [
      Point(x * 10, y * 10),
      Point(x * 100, y * 100)
    ], {
      "a": [Point(x * 1000, x * 1000), Point(x * 1000, y * 1000)],
      "b": [Point(x * 10000, x * 10000), Point(x * 10000, x * 10000)]
    }, [
      [
        {
          "a": [Point(x * 20, y * 20), Point(x * 20, y * 20)],
          "b": [Point(x * 30, y * 30), Point(x * 30, y * 30)]
        }
      ]
    ]);
  }
}
