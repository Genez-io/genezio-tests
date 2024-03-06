#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists
from utils import kill_process

def test_js_sdk():
    print("Starting javascript sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/js-sdk/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("./client/sdk/remote.js") == True, "Remote js sdk not found"
    assert exists("./client/sdk/server.sdk.js") == True, "Class js sdk not found"

    with open("./client/sdk/server.sdk.js", "r") as f:
        content = f.read()

    assert "static async method()" in content, "Wrong exported method without parameters"
    assert "static async methodWithoutParameters()" in content, "Wrong exported method with return type"
    assert "static async methodWithOneParameter(test1)" in content, "Wrong exported method with one parameter"
    assert "static async methodWithMultipleParameters(test1, test2)" in content, "Wrong exported method with multiple parameters"

    os.chdir("../")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("./client/sdk/remote.js") == True, "Remote js sdk not found"
    assert exists("./client/sdk/server.sdk.js") == True, "Class js sdk not found"

    with open("../client/sdk/server.sdk.js", "r") as f:
        content = f.read()

    assert "static async method()" in content, "Wrong exported method without parameters"
    assert "static async methodWithoutParameters()" in content, "Wrong exported method with return type"
    assert "static async methodWithOneParameter(test1)" in content, "Wrong exported method with one parameter"
    assert "static async methodWithMultipleParameters(test1, test2)" in content, "Wrong exported method with multiple parameters"

    kill_process(process)
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_js_sdk()
