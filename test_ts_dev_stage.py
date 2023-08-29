#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists

def test_ts_sdk():
    print("Starting typescript dev stage test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/ts-sdk/server/")
    deploy_result = genezio_deploy(False, args=["dev"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/sdk/remote.ts") == True, "Remote ts sdk not found"
    assert exists("../client/sdk/server.sdk.ts") == True, "Class ts sdk not found"

    f = open("../client/sdk/server.sdk.ts", "r")
    content = f.read()

    assert "static async method()" in content, "Wrong exported method without parameters"
    assert "static async methodWithoutParameters(): Promise<string>" in content, "Wrong exported method with return type"
    assert "static async methodWithOneParameter(test1: string): Promise<string>" in content, "Wrong exported method with one parameter"
    assert "static async methodWithMultipleParameters(test1: string, test2: number): Promise<string>" in content, "Wrong exported method with multiple parameters"

    os.chdir("../server/")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("../client/sdk/remote.ts") == True, "Remote ts sdk not found"
    assert exists("../client/sdk/server.sdk.ts") == True, "Class ts sdk not found"

    f = open("../client/sdk/server.sdk.ts", "r")
    content = f.read()

    assert "static async method()" in content, "Wrong exported method without parameters"
    assert "static async methodWithoutParameters(): Promise<string>" in content, "Wrong exported method with return type"
    assert "static async methodWithOneParameter(test1: string): Promise<string>" in content, "Wrong exported method with one parameter"
    assert "static async methodWithMultipleParameters(test1: string, test2: number): Promise<string>" in content, "Wrong exported method with multiple parameters"

    process.kill()
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_ts_sdk()
