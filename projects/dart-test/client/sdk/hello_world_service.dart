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

  static Future<String> methodWithReturnSimpleString() async {
    final response = await remote.call("HelloWorldService.methodWithReturnSimpleString", []);

    return response as String;
  }

  static Future<int> methodWithReturnSimpleInt() async {
    final response = await remote.call("HelloWorldService.methodWithReturnSimpleInt", []);

    return response as int;
  }

  static Future<bool> methodWithReturnSimpleBool() async {
    final response = await remote.call("HelloWorldService.methodWithReturnSimpleBool", []);

    return response as bool;
  }

  static Future<List<Point>> replacePointsInArray(List<Point> list) async {
    final response = await remote.call("HelloWorldService.replacePointsInArray", [list]);

    return (response as List<dynamic>).map((e) => Point.fromJson(e as Map<String, dynamic>),).toList();
  }

  static Future<Map<String, Point>> replacePointsInMap(Map<String, Point> map) async {
    final response = await remote.call("HelloWorldService.replacePointsInMap", [map]);

    return (response as Map<String, dynamic>).map((k, e) => MapEntry(k,Point.fromJson(e as Map<String, dynamic>),));
  }

  static Future<List<int>> getNumbers(int x, int y, int z) async {
    final response = await remote.call("HelloWorldService.getNumbers", [x, y, z]);

    return (response as List<dynamic>).map((e) => e as int).toList();
  }

  static Future<List<String>> getStrings(String x, String y, String z) async {
    final response = await remote.call("HelloWorldService.getStrings", [x, y, z]);

    return (response as List<dynamic>).map((e) => e as String).toList();
  }

  static Future<List<int>> getNumbersAsFuture(int x, int y, int z) async {
    final response = await remote.call("HelloWorldService.getNumbersAsFuture", [x, y, z]);

    return (response as List<dynamic>).map((e) => e as int).toList();
  }

  static Future<List<Point>> getPoints(int x, int y, int count) async {
    final response = await remote.call("HelloWorldService.getPoints", [x, y, count]);

    return (response as List<dynamic>).map((e) => Point.fromJson(e as Map<String, dynamic>),).toList();
  }

  static Future<List<Point>> getPointsAsync(int x, int y, int count) async {
    final response = await remote.call("HelloWorldService.getPointsAsync", [x, y, count]);

    return (response as List<dynamic>).map((e) => Point.fromJson(e as Map<String, dynamic>),).toList();
  }

  static Future<TestResult> getTestResult() async {
    final response = await remote.call("HelloWorldService.getTestResult", []);

    return TestResult.fromJson(response as Map<String, dynamic>);
  }

  static Future<ComplicatedClass> getComplicatedClass(int x, int y) async {
    final response = await remote.call("HelloWorldService.getComplicatedClass", [x, y]);

    return ComplicatedClass.fromJson(response as Map<String, dynamic>);
  }

}
