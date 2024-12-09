#!/usr/bin/python3

import os

import requests

from genezio import genezio_deploy, genezio_login, genezio_delete

def test_nestjs():
    print("Starting nestjs test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/nestjs/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    genezio_delete(deploy_result.project_id)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_nestjs()
