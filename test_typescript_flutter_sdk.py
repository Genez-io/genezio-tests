#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists
from utils import compare_files, kill_process

def test_typescript_flutter_sdk():
    print("Starting test_typescript_flutter_sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/typescript-flutter-sdk/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/sdk/remote.dart") == True, "Remote dart sdk not found"
    assert exists("../client/sdk/chat_backend.dart") == True, "Class dart sdk not found"

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("../client/sdk/remote.dart") == True, "Remote dart sdk not found"
    assert exists("../client/sdk/chat_backend.dart") == True, "Class dart sdk not found"

    assert compare_files("../client/sdk/chat_backend.dart", "../client/chat_backend.dart.template") == True, "Wrong class sdk content"

    kill_process(process)
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_typescript_flutter_sdk()
