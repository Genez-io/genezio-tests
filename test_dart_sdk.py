#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists

def test_dart_sdk():
    print("Starting dart sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/dart-sdk/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/sdk/remote.dart") == True, "Remote dart sdk not found"
    assert exists("../client/sdk/server.dart") == True, "Class dart sdk not found"

    f = open("../client/sdk/server.dart", "r")
    content = f.read()

    assert "static Future<dynamic> method() async" in content, "Wrong exported method without parameters"
    assert "static Future<dynamic> methodWithoutParameters() async" in content, "Wrong exported method with return type"
    assert "static Future<dynamic> methodWithOneParameter(String test1) async" in content, "Wrong exported method with one parameter"
    assert "static Future<dynamic> methodWithMultipleParameters(String test1, double test2, bool test3) async" in content, "Wrong exported method with multiple parameters"

    os.chdir("../server/")

    process = genezio_local()

    assert exists("../client/sdk/remote.dart") == True, "Remote dart sdk not found"
    assert exists("../client/sdk/server.dart") == True, "Class dart sdk not found"

    f = open("../client/sdk/server.dart", "r")
    content = f.read()

    assert "static Future<dynamic> method() async" in content, "Wrong exported method without parameters"
    assert "static Future<dynamic> methodWithoutParameters() async" in content, "Wrong exported method with return type"
    assert "static Future<dynamic> methodWithOneParameter(String test1) async" in content, "Wrong exported method with one parameter"
    assert "static Future<dynamic> methodWithMultipleParameters(String test1, double test2, bool test3) async" in content, "Wrong exported method with multiple parameters"

    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_dart_sdk()
