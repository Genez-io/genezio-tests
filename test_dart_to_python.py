#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_script, run_node_script, run_npm_run_build, kill_process
from os.path import exists


def test_dart_to_python():
    print("Starting dart sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/dart-srv-python-client/server")
    run_script(["dart", "pub", "get"])
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "100string12hello42True[1, 2, 3]['string1', 'string2', 'string3'][1, 2, 3][{'x': 0, 'y': 0}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}][{'x': 0, 'y': 0}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}][{'x': 11, 'y': 12}, {'x': 13, 'y': 14}, {'x': 15, 'y': 16}]", "Wrong output from python test: " + output
    os.chdir("../server")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    run_npm_run_build()
    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    status, output = run_script(["python3", "main.py"])

    assert status == 0, "Node test script returned non-zero exit code"
    assert output in "100string12hello42True[1, 2, 3]['string1', 'string2', 'string3'][1, 2, 3][{'x': 0, 'y': 0}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}][{'x': 0, 'y': 0}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}][{'x': 11, 'y': 12}, {'x': 13, 'y': 14}, {'x': 15, 'y': 16}]", "Wrong output from python test: " + output

    kill_process(process)
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_dart_to_python()
