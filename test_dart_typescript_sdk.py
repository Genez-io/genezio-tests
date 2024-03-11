#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, delete_project
from os.path import exists
from utils import compare_files, kill_process


def test_dart_typescript_sdk():
    print("Starting test_dart_typescript_sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/dart-typescript-sdk/server")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/node_modules/genezio-remote/dist/cjs/remote.d.ts") == True, "Remote typescript cjs sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/node_modules/genezio-remote/dist/esm/remote.d.ts") == True, "Remote typescript esm sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/esm/task.sdk.d.ts") == True, "Class typescript esm sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/cjs/task.sdk.d.ts") == True, "Class typescript cjs sdk not found"

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/node_modules/genezio-remote/dist/cjs/remote.d.ts") == True, "Remote typescript cjs sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/node_modules/genezio-remote/dist/esm/remote.d.ts") == True, "Remote typescript esm sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/esm/task.sdk.d.ts") == True, "Class typescript esm sdk not found"
    assert exists("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/cjs/task.sdk.d.ts") == True, "Class typescript cjs sdk not found"

    assert compare_files("../client/node_modules/@genezio-sdk/test-dart-typescript-sdk/esm/task.sdk.d.ts",
                         "../client/todo_list.ts.template") == True, "Wrong class sdk content"

    kill_process(process)

    delete_project()
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_dart_typescript_sdk()
