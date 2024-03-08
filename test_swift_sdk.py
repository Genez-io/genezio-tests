#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists
from utils import kill_process


def test_swift_sdk():
    print("Starting swift sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/swift-sdk/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("./client/sdk/remote.swift") == True, "Remote swift sdk not found"
    assert exists("./client/sdk/server.sdk.swift") == True, "Class swift sdk not found"

    with open("./client/sdk/server.sdk.swift", "r") as f:
        content = f.read()

    assert "static func method() async -> Any" in content, "Wrong exported method without parameters"
    assert "static func methodWithoutParameters() async -> String" in content, "Wrong exported method with return type"
    assert "static func methodWithOneParameter(test1: String) async -> String" in content, "Wrong exported method with one parameter"
    assert "static func methodWithMultipleParameters(test1: String, test2: Double) async -> String" in content, "Wrong exported method with multiple parameters"

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("./client/sdk/remote.swift") == True, "Remote swift sdk not found"
    assert exists("./client/sdk/server.sdk.swift") == True, "Class swift sdk not found"

    with open("./client/sdk/server.sdk.swift", "r") as f:
        content = f.read()

    assert "static func method() async -> Any" in content, "Wrong exported method without parameters"
    assert "static func methodWithoutParameters() async -> String" in content, "Wrong exported method with return type"
    assert "static func methodWithOneParameter(test1: String) async -> String" in content, "Wrong exported method with one parameter"
    assert "static func methodWithMultipleParameters(test1: String, test2: Double) async -> String" in content, "Wrong exported method with multiple parameters"

    kill_process(process)
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_swift_sdk()
