#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script, run_npm_run_build

def test_todo_list_ts():
    print("Starting todo_list ts test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/todo-list-ts/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    run_npm_run_build()
    status, output = run_node_script("build/test-todo-list.js")

    assert status == 0, "Node test script returned non-zero exit code"

    components = output.split("\n")

    for i in range(0, 8):
        assert components[i] == "Ok", "Component " + str(i) + " returned wrong output"

    os.chdir("../server/")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    run_npm_run_build()
    status, output = run_node_script("build/test-todo-list.js")

    assert status == 0, "Node test script returned non-zero exit code"

    components = output.split("\n")

    for i in range(0, 8):
        assert components[i] == "Ok", "Component " + str(i) + " returned wrong output"

    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_todo_list_ts()
