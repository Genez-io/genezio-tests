#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete
from utils import run_script, kill_process
from os.path import exists


def test_python_sdk():
    print("Starting python sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/python-sdk/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("./client/sdk/remote.py") == True, "Remote python sdk not found"
    assert exists("./client/sdk/server.py") == True, "Class python sdk not found"

    os.chdir("./client/")

    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "Nonestringstringstring", "Wrong output from python test: " + output
    os.chdir("../")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    assert exists("./client/sdk/remote.py") == True, "Remote python sdk not found"
    assert exists("./client/sdk/server.py") == True, "Class python sdk not found"

    os.chdir("./client/")

    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "Nonestringstringstring", "Wrong output from python test: " + output

    kill_process(process)
    os.chdir("../")
    print("Prepared to delete project...")
    genezio_delete(deploy_result.project_id)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_python_sdk()
