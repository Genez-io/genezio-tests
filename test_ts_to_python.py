#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script, run_npm_run_build, run_script

def test_ts_to_python_sdk():
    print("Starting ts to python sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/typescript-srv-python-client/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "Hello from server!1string2name0typeTrueFalse22[11, 22]", "Wrong output from python test: " + output
    os.chdir("../server/")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    run_npm_run_build()
    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "Hello from server!1string2name0typeTrueFalse22[11, 22]", "Wrong output from python test: " + output

    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_ts_to_python_sdk()
