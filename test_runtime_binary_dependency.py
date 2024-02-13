#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script, kill_process

def test_runtime_linux_binary_dependency():
    print("Starting binary_dependency linux runtime test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/binary-dependency/server/")
    deploy_result = genezio_deploy(False, "./genezio-runtime-linux.yaml",["--install-deps"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    status, output = run_node_script("test-binary-dependency.js")

    assert status == 0, "Node test script returned non-zero exit code"
    assert output == "Ok\n", "Node script returned wrong output"

    os.chdir("../server/")

    process = genezio_local(["--install-deps"])

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    status, output = run_node_script("test-binary-dependency.js")

    assert status == 0, "Node test script returned non-zero exit code"
    assert output == "Ok\n", "Node script returned wrong output"

    kill_process(process)

    os.chdir("../")
    with open("stdout.txt", "r") as f:
        stdout = f.read()
        print(stdout)
    with open("stderr.txt", "r") as f:
        stderr = f.read()
        print(stderr)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_runtime_linux_binary_dependency()
