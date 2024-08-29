#!/usr/bin/python3

import os
import requests
from genezio import genezio_deploy, genezio_delete

def test_genezio_services():
    print("Starting services configuration test...")
    token = os.environ.get('GENEZIO_TOKEN')

    os.chdir("./projects/services-configuration/")
    deploy_result = genezio_deploy(False, with_config="./genezio-database.yaml")

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    is_database_result = get_database("it-gnz-database", token)
    assert is_database_result != None, "Database not created"
    print("Database test passed.")

    deploy_result = genezio_deploy(False, with_config="./genezio-email.yaml")

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    is_email_result = is_email(token)
    assert is_email_result, "Email service not enabled"
    print("Email test passed.")

    deploy_result = genezio_deploy(False, with_config="./genezio-authentication.yaml")

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    is_authentication_result = is_auth("services-configuration", token)
    assert is_authentication_result, "Authentication not enabled"
    auth_providers_result = check_auth_providers("services-configuration", token)
    assert auth_providers_result, "Authentication providers not enabled"
    print("Authentication test passed.")

    print("Cleanup resources...")
    genezio_delete(deploy_result.project_id)
    delete_database("it-gnz-database", token)

    print("Test passed!")

def get_database(name: str, token: str) -> bool:
    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/databases"

    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    # Iterate over the databases to see if any match the provided name
    for db in data.get('databases', []):
        if db.get('name') == name:
            return db.get('id')

    return None

def delete_database(name: str, token: str):
    id = get_database(name, token)
    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/databases/{id}"
    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json().get('status') == 'ok'

def is_email(token: str) -> bool:
    environment = get_backend_environment("services-configuration", token)

    for env in environment:
        if env.get('name') == 'EMAIL_SERVICE_TOKEN':
            return True
    return False

def is_auth(name: str, token: str) -> bool:
    _, envId = get_project_name(name, token)

    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/core/auth/{envId}"
    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    return data.get('enabled')

def check_auth_providers(name: str, token: str) -> bool:
    _, envId = get_project_name(name, token)

    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/core/auth/providers/{envId}"
    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    for provider in data.get('authProviders'):
        if provider.get('enabled') == False:
            return False
    return True


def get_backend_environment(name:str, token: str) -> str:
    projectId, envId = get_project_name(name, token)

    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/projects/{projectId}/{envId}/environment-variables"
    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    return data.get('environmentVariables')

def get_project_name(name: str, token: str):
    backend_endpoint = os.environ.get('GENEZIO_BACKEND_ENDPOINT')
    url = f"https://{backend_endpoint}/projects/name/{name}"
    payload = ""

    headers = {
    'Accept-Version': 'cli/2.4.2',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    projectId = data.get('project').get('id')
    for env in data.get('project').get('projectEnvs'):
        if env.get('name') == 'prod':
            envId = env.get('id')
            break

    return projectId, envId

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_genezio_services()
