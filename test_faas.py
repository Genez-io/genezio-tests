#!/usr/bin/python3

import os

import requests

from genezio import genezio_deploy, genezio_login, genezio_delete

def test_faas_python():
    print("Starting faas_python test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/faas-node/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    genezio_delete(deploy_result.project_id)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_faas_python()
