// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'server.dart';

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
