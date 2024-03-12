#!/usr/bin/python3

import os

import yaml

from genezio import genezio_deploy, genezio_login, genezio_local, genezio_list, genezio_delete
from utils import run_node_script, kill_process


def test_binary_dependency():
    print("Starting binary_dependency test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/binary-dependency/")
    deploy_result = genezio_deploy(deploy_frontend=False, args=["--install-deps"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("./client/")

    status, output = run_node_script("test-binary-dependency.js")

    assert status == 0, "Node test script returned non-zero exit code"
    assert output == "Ok\n", "Node script returned wrong output"

    os.chdir("../")

    process = genezio_local(args=["--install-deps"])

    assert process != None, "genezio local returned None"

    os.chdir("./client/")

    status, output = run_node_script("test-binary-dependency.js")

    assert status == 0, "Node test script returned non-zero exit code"
    assert output == "Ok\n", "Node script returned wrong output"

    kill_process(process)

    os.chdir("../")

    new_project_name = yaml.safe_load(open("./genezio.yaml", "r").read())["name"]

    print("Successfully deployed project: " + new_project_name)
    print("Testing project deletion...")

    # List the project by name
    returncode, _, stdout = genezio_list(new_project_name, True)
    assert returncode == 0, "genezio list <name> returned non-zero exit code"
    assert stdout.__contains__(new_project_name), "genezio list <name> did not list the added project"

    # Get the project id
    project_id = stdout.split("ID: ")[1].split(",")[0]

    # Delete the project
    returncode, stderr, stdout = genezio_delete(project_id)
    assert returncode == 0, "genezio delete returned non-zero exit code"
    assert "Your project has been deleted" in stdout, "genezio delete did not return the correct message"

    # List the projects again to check deleted project
    returncode, _, stdout = genezio_list(None, False)
    assert returncode == 0, "genezio list returned non-zero exit code"
    assert not stdout.__contains__(new_project_name), "genezio list listed the deleted project"

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_binary_dependency()
