// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'hello_world.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Point _$PointFromJson(Map<String, dynamic> json) => Point(
      json['x'] as int,
      json['y'] as int,
    );

Map<String, dynamic> _$PointToJson(Point instance) => <String, dynamic>{
      'x': instance.x,
      'y': instance.y,
    };

TestResult _$TestResultFromJson(Map<String, dynamic> json) => TestResult(
      json['number'] as int,
      json['string'] as String,
      Point.fromJson(json['point'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$TestResultToJson(TestResult instance) =>
    <String, dynamic>{
      'number': instance.number,
      'string': instance.string,
      'point': instance.point,
    };

ComplicatedClass _$ComplicatedClassFromJson(Map<String, dynamic> json) =>
    ComplicatedClass(
      Point.fromJson(json['a'] as Map<String, dynamic>),
      Point.fromJson(json['b'] as Map<String, dynamic>),
      (json['otherPoints'] as List<dynamic>)
          .map((e) => Point.fromJson(e as Map<String, dynamic>))
          .toList(),
      (json['pointsMap'] as Map<String, dynamic>).map(
        (k, e) => MapEntry(
            k,
            (e as List<dynamic>)
                .map((e) => Point.fromJson(e as Map<String, dynamic>))
                .toList()),
      ),
      (json['pointsMap2'] as List<dynamic>)
          .map((e) => (e as List<dynamic>)
              .map((e) => (e as Map<String, dynamic>).map(
                    (k, e) => MapEntry(
                        k,
                        (e as List<dynamic>)
                            .map((e) =>
                                Point.fromJson(e as Map<String, dynamic>))
                            .toList()),
                  ))
              .toList())
          .toList(),
    );

Map<String, dynamic> _$ComplicatedClassToJson(ComplicatedClass instance) =>
    <String, dynamic>{
      'a': instance.a,
      'b': instance.b,
      'otherPoints': instance.otherPoints,
      'pointsMap': instance.pointsMap,
      'pointsMap2': instance.pointsMap2,
    };
