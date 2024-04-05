#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_list

# This test is meant to assure that deploying on a collaborative project still works.
# The testing account that logs in to deploy is an admin on the project, not the owner.
#
# To make sure this test is successful:
# 1. The deployment has to be successful
# 2. There should be a single project named `collaboration-project` deployed.
# If there are 2 something went wrong.
def test_collaboration():
    print("Starting collaboration test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    project_name = "collaboration-project"
    os.chdir("./projects/hello-world/")
    deploy_result = genezio_deploy(False, with_config="./genezio-collaboration.yaml")

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    returncode, stderr, stdout = genezio_list(project_name, False)
    assert returncode == 0, "genezio list failed with:" + stderr
    assert "There is no project with this identifier" not in stdout, "project not found"

    project_names = extract_project_names(stdout)
    assert len(project_names) == 1, "found more than 1 project with the same name"

    print("Test passed!")

def extract_project_names(stdout):
    # Split the stdout into lines
    lines = stdout.split('\n')

    # Extract project names from the lines
    project_names = []
    for line in lines:
        if "Project name:" in line:
            # Extract the project name from the line
            project_name = line.split("Project name: ")[1].split(',')[0].strip()
            project_names.append(project_name)

    return project_names

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_collaboration()
