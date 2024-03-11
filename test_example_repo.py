#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, delete_project
from utils import kill_process


def test_example_repo(language: str, repo_name_example: str, path: str):
    print("Starting {} test...".format(language + " " + repo_name_example))
    token = os.environ.get('GENEZIO_TOKEN')

    os.chdir(os.path.join(path, "projects", "examples", "genezio-examples", language, repo_name_example))

    genezio_login(token)

    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    process = genezio_local()

    assert process != None, "genezio local returned None"
    kill_process(process)

    delete_project()
    print("Test passed!")
