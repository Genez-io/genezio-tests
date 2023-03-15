#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login
from utils import run_curl

def test_frontend():
    print("Starting frontend test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/mini-frontend/server/")

    deploy_result = genezio_deploy(True)

    assert deploy_result.return_code == 0, "genezio deploy --frontend returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy --frontend returned empty project url"
    assert "mnopqr-genezio-test-frontend" in deploy_result.project_url, "genezio deploy --frontend returned wrong project url"

    status, output = run_curl(deploy_result.project_url)
    assert status == 0, "`curl` returned non-zero exit code"
    assert "Hello World" in output, "page " + deploy_result.project_url + " doesn't contain 'Hello World'"

    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_frontend()
