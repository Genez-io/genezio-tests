#!/usr/bin/python3

import os
import shutil
import yaml
from genezio import genezio_login, genezio_deploy, genezio_list, genezio_delete

def test_create_list_delete():
    print("Starting listing test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)   

    os.chdir("./projects/listing/")

    new_project_name = yaml.safe_load(open("./genezio.yaml", "r").read())["name"]

    # Deploy the project
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    # List the projects
    returncode, _, stdout = genezio_list(None, False)
    assert returncode == 0, "genezio list returned non-zero exit code"
    assert stdout.__contains__(new_project_name), "genezio ls did not list the added project"

    projects = stdout.split("\n")
    projects = list(filter(lambda x: x != "", projects))
    projects = list(filter(lambda x: x.__contains__(new_project_name), projects))
    assert len(projects) == 1, "genezio list listed more than one project with the same name"

    # List the project by name
    returncode, _, stdout = genezio_list(new_project_name, True)
    assert returncode == 0, "genezio list <name> returned non-zero exit code"
    assert stdout.__contains__(new_project_name), "genezio list <name> did not list the added project"
    
    # Get the project id
    project_id = stdout.split("ID: ")[1].split(",")[0]

    # Delete the project
    returncode, stderr, stdout = genezio_delete(project_id)
    assert returncode == 0, "genezio delete returned non-zero exit code"
    assert stderr == "", "genezio delete returned non-empty stderr"
    assert "Your project has been deleted" in stdout, "genezio delete did not return the correct message"

    # List the projects again to check deleted project
    returncode, _, stdout = genezio_list(None, False)
    assert returncode == 0, "genezio list returned non-zero exit code"
    assert not stdout.__contains__(new_project_name), "genezio list listed the deleted project"

    # cleanup
    os.chdir("../../")
    shutil.rmtree("./projects/listing/sdk")

    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_create_list_delete()