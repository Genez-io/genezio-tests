#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login
from utils import run_npm_build, run_wget

def test_frontend():
    print("Starting frontend test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/mini-frontend/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    status = run_npm_build()
    assert status == 0, "`npm run build` returned non-zero exit code"

    os.chdir("../server/")

    deploy_result = genezio_deploy(True)

    assert deploy_result.return_code == 0, "genezio deploy --frontend returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy --frontend returned empty project url"
    assert "asdfghj-genezio-test-frontend" in deploy_result.project_url, "genezio deploy --frontend returned wrong project url"

    status = run_wget(deploy_result.project_url)
    assert status == 0, "`wget` returned non-zero exit code"

    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_frontend()
