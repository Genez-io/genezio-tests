#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists

def test_hello():
    print("Starting swift sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/swift-sdk/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/sdk/remote.swift") == True, "Remote swift sdk not found"
    assert exists("../client/sdk/server.sdk.swift") == True, "Remote swift sdk not found"
    
    f = open("../client/sdk/server.sdk.swift", "r")
    content = f.read()

    assert "static func method() async -> Any" in content, "Wrong exported method without parameters"
    assert "static func methodWithoutParameters() async -> String" in content, "Wrong exported method with return type" 
    assert "static func methodWithOneParameter(test1: String) async -> String" in content, "Wrong exported method with one parameter"
    assert "static func methodWithMultipleParameters(test1: String, test2: Double) async -> String" in content, "Wrong exported method with multiple parameters"

    os.chdir("../server/")

    process = genezio_local()

    assert exists("../client/sdk/remote.swift") == True, "Remote swift sdk not found"
    assert exists("../client/sdk/server.sdk.swift") == True, "Remote swift sdk not found"
    
    f = open("../client/sdk/server.sdk.swift", "r")
    content = f.read()

    assert "static func method() async -> Any" in content, "Wrong exported method without parameters"
    assert "static func methodWithoutParameters() async -> String" in content, "Wrong exported method with return type" 
    assert "static func methodWithOneParameter(test1: String) async -> String" in content, "Wrong exported method with one parameter"
    assert "static func methodWithMultipleParameters(test1: String, test2: Double) async -> String" in content, "Wrong exported method with multiple parameters"


    process.kill()
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_hello()