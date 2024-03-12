#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete
from os.path import exists
from utils import kill_process


def check_output():
    assert exists(
        "./client/node_modules/@genezio-sdk/typescript-sdk-example/lib/server.sdk.d.ts") == True, "Class ts lib sdk not found"
    assert exists(
        "./client/node_modules/@genezio-sdk/typescript-sdk-example/node_modules/genezio-remote/dist/lib/remote.d.ts") == True, "Remote ts sdk lib not found"

    with open("./client/node_modules/@genezio-sdk/typescript-sdk-example/lib/server.sdk.d.ts", "r",  encoding="utf-8") as f:
        content = f.read()

    assert "static method(): Promise<any>" in content, "Wrong exported method without parameters"
    assert "static methodWithoutParameters(): Promise<string>" in content, "Wrong exported method with return type"
    assert "static methodWithOneParameter(test1: string): Promise<string>" in content, "Wrong exported method with one parameter"
    assert "static methodWithMultipleParameters(test1: string, test2: number): Promise<string>" in content, "Wrong exported method with multiple parameters"


def test_ts_sdk_dev_stage():
    print("Starting typescript dev stage test...")
    token = os.environ.get('GENEZIO_TOKEN')

    if os.path.exists("./projects/ts-sdk/client") is False:
        os.makedirs("./projects/ts-sdk/client")

    genezio_login(token)

    os.chdir("./projects/ts-sdk/")
    deploy_result = genezio_deploy(False, args=["--stage", "dev"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    check_output()

    process = genezio_local()

    assert process is not None, "genezio local returned None"

    check_output()
    kill_process(process)

    print("Prepared to delete project...")
    genezio_delete(deploy_result.project_id)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_ts_sdk_dev_stage()
