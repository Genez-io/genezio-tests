/// This is an auto generated code. This code should not be modified since the file can be overwritten
/// if new genezio commands are executed.

import 'remote.dart';


class Point {
    int x;
    int y;
  
    Point(this.x,this.y,);

    factory Point.fromJson(Map<String, dynamic> json) => Point(json['x'] as int,json['y'] as int,);
    
    Map<String, dynamic> toJson() => <String, dynamic>{"x": x,"y": y,};
}


class TestResult {
    int number;
    String string;
    Point point;
  
    TestResult(this.number,this.string,this.point,);

    factory TestResult.fromJson(Map<String, dynamic> json) => TestResult(json['number'] as int,json['string'] as String,Point.fromJson(json['point'] as Map<String, dynamic>),);
    
    Map<String, dynamic> toJson() => <String, dynamic>{"number": number,"string": string,"point": point,};
}


class ComplicatedClass {
    Point a;
    Point b;
    List<Point> otherPoints;
    Map<String, List<Point>> pointsMap;
    List<List<Map<String, List<Point>>>> pointsMap2;
  
    ComplicatedClass(this.a,this.b,this.otherPoints,this.pointsMap,this.pointsMap2,);

    factory ComplicatedClass.fromJson(Map<String, dynamic> json) => ComplicatedClass(Point.fromJson(json['a'] as Map<String, dynamic>),Point.fromJson(json['b'] as Map<String, dynamic>),(json['otherPoints'] as List<dynamic>).map((e) => Point.fromJson(e as Map<String, dynamic>),).toList(),(json['pointsMap'] as Map<String, dynamic>).map((k, e) => MapEntry(k,(e as List<dynamic>).map((e) =>Point.fromJson(e as Map<String, dynamic>),).toList())),(json['pointsMap2'] as List<dynamic>).map((e) => (e as List<dynamic>).map((e) =>(e as Map<String, dynamic>).map((k, e) => MapEntry(k,(e as List<dynamic>).map((e) =>Point.fromJson(e as Map<String, dynamic>),).toList()))).toList()).toList(),);
    
    Map<String, dynamic> toJson() => <String, dynamic>{"a": a,"b": b,"otherPoints": otherPoints,"pointsMap": pointsMap,"pointsMap2": pointsMap2,};
}


class HelloWorldService {
  static final remote = Remote("http://127.0.0.1:8083/HelloWorldService");

  static Future<void> methodWithVoidReturnVoid() async {
    await remote.call("HelloWorldService.methodWithVoidReturnVoid", []);
  }

  static Future<void> methodWithStringReturnVoid(String string) async {
    await remote.call("HelloWorldService.methodWithStringReturnVoid", [string]);
  }

  static Future<void> methodWithPointReturnVoid(Point point) async {
    await remote.call("HelloWorldService.methodWithPointReturnVoid", [point]);
  }

  static Future<List<int>> getNumbers(int x, int y, int z) async {
    final response = await remote.call("HelloWorldService.getNumbers", [x, y, z]);

    return response as List<int>;
  }

  static Future<List<String>> getStrings(String x, String y, String z) async {
    final response = await remote.call("HelloWorldService.getStrings", [x, y, z]);

    return response as List<String>;
  }

  static Future<List<int>> getNumbersAsFuture(int x, int y, int z) async {
    final response = await remote.call("HelloWorldService.getNumbersAsFuture", [x, y, z]);

    return response as List<int>;
  }

  static Future<TestResult> getTestResult() async {
    final response = await remote.call("HelloWorldService.getTestResult", []);

    return TestResult.fromJson(response);
  }

  static Future<ComplicatedClass> getComplicatedClass(int x, int y) async {
    final response = await remote.call("HelloWorldService.getComplicatedClass", [x, y]);

    return ComplicatedClass.fromJson(response);
  }

}
