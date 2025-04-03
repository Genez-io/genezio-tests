#!/usr/bin/python3

import os
import re

import requests

from genezio import genezio_deploy, genezio_list, genezio_login, genezio_delete

def extract_project_id(output: str) -> str:
    match = re.search(r"ID:\s*([a-f0-9\-]+)", output, re.IGNORECASE)
    if match:
        return match.group(1)
    raise ValueError("Project ID not found in the output.")

def test_environment_variables():
    print("Starting faas_environment_variables test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/faas-node/")

    deploy_result = genezio_deploy(False, args=["--config", "./genezio-backend-environment-wrong-resource.yaml"])
    assert deploy_result.return_code != 0, "genezio deploy returned zero exit code - expected error"
    assert "The attribute missing-function from backend.functions.missing-function is not supported or does not exist in the given resource" in deploy_result.stderr, "expected error message not found in stderr"

    deploy_result = genezio_deploy(False, args=["--config", "./genezio-backend-environment-wrong-attribute.yaml"])
    assert deploy_result.return_code != 0, "genezio deploy returned zero exit code - expected error"
    assert "The attribute test is not supported for function hello-world. You can use one of the following attributes: name, path, handler, entry, type and url" in deploy_result.stderr, "expected error message not found in stderr"

    deploy_result = genezio_deploy(False, args=["--config", "./genezio-backend-environment-env-file-not-found.yaml"])
    assert deploy_result.return_code != 0, "genezio deploy returned zero exit code - expected error"
    assert "Environment variable file was not provided" in deploy_result.stderr, "expected error message not found in stderr"

    # Deploy without setting the environment variables
    deploy_result = genezio_deploy(False, args=["--config", "./genezio-backend-environment.yaml"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    env = response.json()["env"]

    # Define a regex pattern to match any UUID
    uuid_pattern = r"https://[a-f0-9\-]+\.(us-east-1|dev-fkt)\.cloud\.genez\.io"

    assert "CLEARTEXT_ENV_VAR" in env, "Missing CLEARTEXT_ENV_VAR in response"
    assert env["CLEARTEXT_ENV_VAR"] == "my-value", "Function did not receive the correct environment variables, actual value: " + env["CLEARTEXT_ENV_VAR"]
    assert "HELLO_WORLD_FUNCTION_URL" in env, "Missing HELLO_WORLD_FUNCTION_URL in response"
    assert re.match(uuid_pattern, env["HELLO_WORLD_FUNCTION_URL"]), "Function URL does not match expected pattern, actual value: " + env["HELLO_WORLD_FUNCTION_URL"]

    genezio_delete(deploy_result.project_id)

    print("Test passed!")


def test_environment_variables_with_env_file():
    print("Starting faas_environment_variables with environment file test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/faas-node-env-file/")

    deploy_result = genezio_deploy(False, args=["--env", ".env.wrong"])

    assert deploy_result.return_code != 0, "genezio deploy returned zero exit code - expected error"
    assert ".env.wrong does not exist" in deploy_result.stderr, "expected error message not found in stderr"

    # Deploy without setting the environment variables
    # Note: it's important that this is a first time deployment, otherwise the environment variables will not be missing
    project_details = genezio_list("test-environment-variables-with-env")
    project_id = extract_project_id(project_details)
    genezio_delete(project_id)

    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert "Environment variables SECRET_ENV_VAR, TEST_ENV_VAR are not set remotely" in deploy_result.stdout, "could not detect missing environment variables"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    deploy_result = genezio_deploy(False, args=["--env", ".env"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    env = response.json()["env"]

    assert "SECRET_ENV_VAR" in env, "Missing SECRET_ENV_VAR in response"
    assert env["SECRET_ENV_VAR"] == "secret-value", "Function did not receive the correct environment variables, actual value: " + env["SECRET_ENV_VAR"]

    assert "TEST_ENV_VAR" in env, "Missing TEST_ENV_VAR in response"
    assert env["TEST_ENV_VAR"] == "value", "Function did not receive the correct environment variables, actual value: " + env["TEST_ENV_VAR"]

    deploy_result = genezio_deploy(False, args=["--env", "secrets/.env.test"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    env = response.json()["env"]

    assert "TEST_SECOND_ENV_VAR" in env, "Missing TEST_SECOND_ENV_VAR in response"
    assert env["TEST_SECOND_ENV_VAR"] == "value-second", "Function did not receive the correct environment variables, actual value: " + env["TEST_SECOND_ENV_VAR"]

    genezio_delete(deploy_result.project_id)

    deploy_result = genezio_deploy(False, args=["--env", ".env", "--config", "./genezio-backend-environment.yaml"])

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    response = requests.get(deploy_result.web_urls[0])
    print(response.json())

    assert response.status_code == 200, "Function returned non-200 status code"
    assert response.json()["status"] == "success", "Function returned wrong output"

    env = response.json()["env"]

    assert "SECRET_ENV_VAR" in env, "Missing SECRET_ENV_VAR in response"
    assert env["SECRET_ENV_VAR"] == "secret-value", "Function did not receive the correct environment variables, actual value: " + env["SECRET_ENV_VAR"]

    assert "TEST_ENV_VAR" in env, "Missing TEST_ENV_VAR in response"
    assert env["TEST_ENV_VAR"] == "value", "Function did not receive the correct environment variables, actual value: " + env["TEST_ENV_VAR"]

    # Define a regex pattern to match any UUID
    uuid_pattern = r"https://[a-f0-9\-]+\.(us-east-1|dev-fkt)\.cloud\.genez\.io"

    assert "CLEARTEXT_ENV_VAR" in env, "Missing CLEARTEXT_ENV_VAR in response"
    assert env["CLEARTEXT_ENV_VAR"] == "my-value", "Function did not receive the correct environment variables, actual value: " + env["CLEARTEXT_ENV_VAR"]
    assert "HELLO_WORLD_FUNCTION_URL" in env, "Missing HELLO_WORLD_FUNCTION_URL in response"
    assert re.match(uuid_pattern, env["HELLO_WORLD_FUNCTION_URL"]), "Function URL does not match expected pattern, actual value: " + env["HELLO_WORLD_FUNCTION_URL"]

    genezio_delete(deploy_result.project_id)

    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_environment_variables()
    os.chdir("../..")
    test_environment_variables_with_env_file()
