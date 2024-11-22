#!/usr/bin/python3

import os
import requests
from genezio import genezio_deploy, genezio_login, genezio_delete, genezio_local
import time

def wait_for_server(url, max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            print(f"Server not ready, attempt {i+1}/{max_retries}. Waiting {delay} seconds...")
            time.sleep(delay)
    return False

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

        process = genezio_local()
        assert process != None, "genezio local returned None"
        print("Local server started", process)

        # Wait for server to be ready
        url = "http://localhost:8090"
        assert wait_for_server(url), "Server failed to start after maximum retries"
        print("Local server is ready")

        # Test home route locally
        response = requests.get(f'{url}/')
        assert response.status_code == 200, f"Expected status code 200 for local home route, got {response.status_code}"
        assert response.text == 'Hello, World!', f"Expected 'Hello, World!' for local home route, got {response.text}"
        print("Local home route test passed")

        # Test name route locally
        name = 'Alice'
        response = requests.get(f'{url}/name', params={'name': name})
        assert response.status_code == 200, f"Expected status code 200 for local name route with parameter, got {response.status_code}"
        assert response.text == f'Hello, {name}!', f"Expected 'Hello, {name}!' for local name route, got {response.text}"
        print("Local name route with parameter test passed")

        # Test name route with no parameters locally
        response = requests.get(f'{url}/name')
        assert response.status_code == 200, f"Expected status code 200 for local name route without parameter, got {response.status_code}"
        assert response.text == 'Hello, Unknown!', f"Expected 'Hello, Unknown!' for local name route without parameter, got {response.text}"
        print("Local name route without parameter test passed")

        # Test stream route locally
        response = requests.get(f'{url}/stream', stream=True)
        assert response.status_code == 200, f"Expected status code 200 for local stream route, got {response.status_code}"
        chunks = list(response.iter_lines())
        assert len(chunks) == 5, f"Expected 5 chunks from local stream route, got {len(chunks)}"
        for i, chunk in enumerate(chunks):
            expected_chunk = f'Chunk {i}'
            assert chunk.decode('utf-8') == expected_chunk, f"Expected '{expected_chunk}' in local stream, got '{chunk.decode('utf-8')}'"
        print("Local stream route test passed")

        # Test POST data route with valid data locally
        data = {"key": "value"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{url}/post-data', json=data, headers=headers)
        assert response.status_code == 200, f"Expected status code 200 for local POST data with valid data, got {response.status_code}"
        assert response.json() == data, f"Expected response JSON {data} for local route, got {response.json()}"
        print("Local POST data route with data test passed")

        process.terminate()
        process.wait()

    finally:
        # Cleanup: delete the deployed project
        genezio_delete(deploy_result.project_id)
        print("Project deleted and cleanup completed")

    print("All tests passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_flask_python()
