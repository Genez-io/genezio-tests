#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists

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

    f = open("../client/sdk/chat_backend.dart", "r")
    content = f.read()
    
    template_content = open("../client/chat_backend.dart.template", "r").read()

    assert content == template_content, "Wrong class sdk content"

    process.kill()
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_typescript_flutter_sdk()
