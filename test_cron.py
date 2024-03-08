#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script, kill_process
import time


def test_hello():
    print("Starting cron test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/crons/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("./client/")

    status, output = run_node_script("test-cron.js")

    assert status == 0, "Node test script returned non-zero exit code"
    number = int(output)
    print("Testing on remote server...")
    print("First request. Number is " + str(number))

    time.sleep(61)

    status, output = run_node_script("test-cron.js")

    assert status == 0, "Node test script returned non-zero exit code"
    numberAfterOneMinute = int(output)
    print("Second request. Number is " + str(numberAfterOneMinute))

    assert numberAfterOneMinute > number, "Cron job did not run"

    os.chdir("../")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("./client/")

    status, output = run_node_script("test-cron.js")

    assert status == 0, "Node test script returned non-zero exit code"
    number = int(output)
    print("Testing on local server...")
    print("First request. Number is " + str(number))

    time.sleep(61)

    status, output = run_node_script("test-cron.js")

    assert status == 0, "Node test script returned non-zero exit code"
    numberAfterOneMinute = int(output)

    print("Second request. Number is " + str(numberAfterOneMinute))

    assert numberAfterOneMinute > number, "Cron job did not run"

    kill_process(process)
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_hello()
