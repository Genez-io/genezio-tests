#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script

def test_lambda_handler_errors():
    print("Starting test_lambda_handler_errors test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/lambda-handler-errors/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code " + deploy_result.return_code
    assert deploy_result.project_url != "", "genezio deploy returned empty project url " + deploy_result.project_url

    os.chdir("../client/")

    status, output = run_node_script("test.js")

    assert status == 0, "Node test script returned non-zero exit code " + status
    assert output == "Error: Error from server\n", "Node script returned wrong output " + output

    os.chdir("../server/")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    status, output = run_node_script("test.js")

    assert status == 0, "Node test script returned non-zero exit code " + status
    assert output == "Error: Error from server\n", "Node script returned wrong output " + output

    process.kill()
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_lambda_handler_errors()