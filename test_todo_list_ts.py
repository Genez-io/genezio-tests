#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, delete_project
from utils import run_node_script, run_npm_run_build, kill_process


def test_todo_list_ts():
    print("Starting todo_list ts test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir(os.path.join('projects', 'todo-list-ts'))
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    process = genezio_local()

    assert process != None, "genezio local returned None"
    os.chdir("./client")

    run_npm_run_build()
    status, output = run_node_script(os.path.join('build', 'test-todo-list.js'))

    assert status == 0, "Node test script returned non-zero exit code"

    components = output.split("\n")

    for i in range(0, 8):
        assert components[i] == "Ok", "Component " + str(i) + " returned wrong output"

    kill_process(process)
    os.chdir("../")
    delete_project()

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_todo_list_ts()
