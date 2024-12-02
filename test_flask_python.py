#!/usr/bin/python3

import os
import requests
from genezio import genezio_deploy, genezio_login, genezio_delete, genezio_local
from utils import create_python_environment, activate_python_environment, pip_install_requirements, deactivate_python_environment
import re

def test_flask_python():
    print("Starting flask_python test...")
    token = os.environ.get('GENEZIO_TOKEN')

    # Login to genezio
    genezio_login(token)

    # Change to the project directory and deploy
    os.chdir("./projects/flask-getting-started/")
    deploy_result = genezio_deploy(False)

    # Assert deployment was successful
    assert deploy_result.return_code == 0, "genezio deploy returned a non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned an empty project URL"

    # Extract the deployed URL for testing
    url = deploy_result.web_urls[0]

    # Test each endpoint
    try:
        # Test home route
        response = requests.get(f'{url}/')
        assert response.status_code == 200, f"Expected status code 200 for home route, got {response.status_code}"
        assert response.text == 'Hello, World!', f"Expected 'Hello, World!' for home route, got {response.text}"
        print("Home route test passed")

        # Test name route
        name = 'Alice'
        response = requests.get(f'{url}/name', params={'name': name})
        assert response.status_code == 200, f"Expected status code 200 for name route with parameter, got {response.status_code}"
        assert response.text == f'Hello, {name}!', f"Expected 'Hello, {name}!' for name route, got {response.text}"
        print("Name route with parameter test passed")

        # Test name route with no parameters
        response = requests.get(f'{url}/name')
        assert response.status_code == 200, f"Expected status code 200 for name route without parameter, got {response.status_code}"
        assert response.text == 'Hello, Unknown!', f"Expected 'Hello, Unknown!' for name route without parameter, got {response.text}"
        print("Name route without parameter test passed")

        # Test stream route
        response = requests.get(f'{url}/stream', stream=True)
        assert response.status_code == 200, f"Expected status code 200 for stream route, got {response.status_code}"
        chunks = list(response.iter_lines())
        assert len(chunks) == 5, f"Expected 5 chunks from stream route, got {len(chunks)}"
        for i, chunk in enumerate(chunks):
            expected_chunk = f'Chunk {i}'
            assert chunk.decode('utf-8') == expected_chunk, f"Expected '{expected_chunk}' in stream, got '{chunk.decode('utf-8')}'"
        print("Stream route test passed")

        # Test POST data route with valid data
        data = {"key": "value"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{url}/post-data', json=data, headers=headers)
        assert response.status_code == 200, f"Expected status code 200 for POST data with valid data, got {response.status_code}"
        assert response.json() == data, f"Expected response JSON {data}, got {response.json()}"
        print("POST data route with data test passed")

        # Test local environment
        local_result = genezio_local()
        path_to_stdout = os.path.join("..", "stdout.txt")
        with open(path_to_stdout, "r", encoding='utf-8') as f:
            stdout = f.read()
            # Extract the local URL from stdout using regex
            match = re.search(r'http://localhost:\d+', stdout)
            if match:
                local_url = match.group(0)
            else:
                raise ValueError("Local URL not found in stdout")

        # Test home local route
        response = requests.get(f'{local_url}/')
        assert response.status_code == 200, f"Expected status code 200 for home route, got {response.status_code}"
        assert response.text == 'Hello, World!', f"Expected 'Hello, World!' for home route, got {response.text}"
        print("Home route local test passed")

        # Test name local route
        response = requests.get(f'{local_url}/name', params={'name': 'Alice'})
        assert response.status_code == 200, f"Expected status code 200 for name route with parameter, got {response.status_code}"
        assert response.text == 'Hello, Alice!', f"Expected 'Hello, Alice!' for name route, got {response.text}"
        print("Name route with parameter local test passed")

        # Test stream local route
        response = requests.get(f'{local_url}/stream', stream=True)
        assert response.status_code == 200, f"Expected status code 200 for stream route, got {response.status_code}"
        chunks = list(response.iter_lines())
        assert len(chunks) == 5, f"Expected 5 chunks from stream route, got {len(chunks)}"
        for i, chunk in enumerate(chunks):
            expected_chunk = f'Chunk {i}'
            assert chunk.decode('utf-8') == expected_chunk, f"Expected '{expected_chunk}' in stream, got '{chunk.decode('utf-8')}'"
        print("Stream route local test passed")

        # Test POST data local route
        data = {"key": "value"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{local_url}/post-data', json=data, headers=headers)
        assert response.status_code == 200, f"Expected status code 200 for POST data with valid data, got {response.status_code}"
        assert response.json() == data, f"Expected response JSON {data}, got {response.json()}"
        print("POST data route with data local test passed")

        # Deactivate the python environment
        deactivate_python_environment_result = deactivate_python_environment()
        assert deactivate_python_environment_result[0] == 0, "deactivate_python_environment returned a non-zero exit code"
        print("Deactivate python environment test passed")

    finally:
        # Cleanup: delete the deployed project
        genezio_delete(deploy_result.project_id)
        print("Project deleted and cleanup completed")

    print("All tests passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_flask_python()
