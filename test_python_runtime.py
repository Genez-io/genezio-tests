#!/usr/bin/python3

import os
import re
import requests
import yaml
from genezio import genezio_deploy, genezio_login, genezio_delete

def install_genezio_from_sources(environment, checkout):
    """
    Clone the Genezio repository and install a specific version from source.
    """
    repo_url = "https://github.com/genez-io/genezio.git"
    os.system("rm -rf genezio && git clone {}".format(repo_url))
    os.chdir("genezio")
    os.system("git checkout v{} -b temp-{}".format(checkout, checkout))

    dependencies_install = "npm install"
    os.system(dependencies_install)

    install_command = "npm run install-locally" if environment == "main" else "npm run install-locally-dev"
    os.system(install_command)
    os.chdir("..")

def update_genezio_yaml_python_runtime(runtime_version):
    """
    Update the genezio.yaml file to set a specific Python runtime version.
    """

    with open("./genezio.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Update the runtime version
    config["backend"]["language"]["runtime"] = f"python{runtime_version}.x"

    with open("./genezio.yaml", "w") as file:
        yaml.safe_dump(config, file, sort_keys=False)

def extract_url_from_output(output):
    """
    Extract the deployed project URL from Genezio CLI output.
    """
    match = re.search(r'https://[a-z0-9-]+\.[a-z0-9-]+\.cloud\.genez\.io', output)
    return match.group(0) if match else None

def check_python_runtime(url, expected_version):
    """
    Make a request to the deployed service and assert the Python version.
    """
    response = requests.get(url)
    assert response.status_code == 200, "Failed to reach deployed service"
    assert expected_version in response.text, f"Expected Python version {expected_version} not found in response"

def test_python_runtimes():
    print("Starting test_python_runtimes test...")
    token = os.environ.get('GENEZIO_TOKEN')

    # Install genezio 3.1.1
    install_genezio_from_sources("dev", "3.1.1")
    genezio_login(token)

    # Deploy a Python legacy runtime (3.11)
    os.chdir("./projects/python-test-runtimes/")
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    project_url = extract_url_from_output(deploy_result.stdout)
    assert project_url, "Failed to extract project URL"
    check_python_runtime(project_url, "3.11")

    # Deploy a specific Python runtime (3.12)
    update_genezio_yaml_python_runtime("3.12")
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    check_python_runtime(project_url, "3.12")

    # Clean up
    genezio_delete(deploy_result.project_id)
    os.chdir("../..")

    # Install genezio 3.1.2
    install_genezio_from_sources("dev", "main")
    genezio_login(token)

    # Deploy a Python default runtime (3.12)
    os.chdir("./projects/python-test-runtimes/")
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    check_python_runtime(project_url, "3.13")

    # Deploy a specific Python runtime (3.12)
    update_genezio_yaml_python_runtime("3.12")
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    check_python_runtime(project_url, "3.12")

    # Clean up
    genezio_delete(deploy_result.project_id)
    print("Test passed!")

if __name__ == '__main__':
    test_python_runtimes()
