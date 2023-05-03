/// This is an auto generated code. This code should not be modified since the file can be overwritten
/// if new genezio commands are executed.

import 'remote.dart';


class ChatBackend {
  static final remote = Remote("http://127.0.0.1:8083/ChatBackend");

  static Future<String> askChatGpt(String prompt, String question) async {
    final response = await remote.call("ChatBackend.askChatGpt", [prompt, question]);

    return response as String;
  }

  static Future<String> askYoda(String question) async {
    final response = await remote.call("ChatBackend.askYoda", [question]);

    return response as String;
  }

  static Future<String> askChewbacca(String question) async {
    final response = await remote.call("ChatBackend.askChewbacca", [question]);

    return response as String;
  }

  static Future<String> addBookmark(String content) async {
    final response = await remote.call("ChatBackend.addBookmark", [content]);

    return response as String;
  }

  static Future<List<String>> getAllBookmarks() async {
    final response = await remote.call("ChatBackend.getAllBookmarks", []);

    return (response as List<dynamic>).map((e) => e as String).toList();
  }

}
