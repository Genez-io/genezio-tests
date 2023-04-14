#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_script
from os.path import exists

def test_dart():
    print("Starting dart sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/dart-test/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")
    run_script(["dart", "pub", "get"])
    os.chdir("../server/")

    status, output = run_script(["dart", "run", "../client/main.dart"])

    print(output)
    assert "100Hello World121 21 210 20100 200a1000 10001000 2000b10000 1000010000 10000a20 4020 40b30 6030 60" in output, "Wrong output from dart test"

    output = ""
    process = genezio_local()

    status, output = run_script(["dart", "run","../client/main.dart"])

    print(output)
    assert "100Hello World121 21 210 20100 200a1000 10001000 2000b10000 1000010000 10000a20 4020 40b30 6030 60" in output, "Wrong output from dart test"
    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_dart()
