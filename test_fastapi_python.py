#!/usr/bin/python3

import os
import requests
from genezio import genezio_deploy, genezio_login, genezio_delete, genezio_local
import time

def test_fastapi_python():
    print("Starting fastapi_python test...")
    # token = os.environ.get("GENEZIO_TOKEN")
    token = "090ce326d7e108cc4c76194fb4fe522784dd4d4ab24315d95cd805f1c53e21dd64290a52e0e34d6d13c3971ef76a512a0d603aec915846578b0b8c358fa6ef85"
    # Login to genezio
    genezio_login(token)

    # Change to the project directory and deploy
    os.chdir("./projects/fastapi/")
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
        print(url)
        assert response.status_code == 200
        assert response.text == '"Hello, World!"'
        print("Home route test passed")

        # Test name route
        name = 'Alice'
        response = requests.get(f'{url}/name', params={'name': name})
        assert response.status_code == 200
        assert response.text == f'"Hello, {name}!"'
        print("Name route with parameter test passed")

        # Test name route with no parameters
        response = requests.get(f'{url}/name')
        assert response.status_code == 200
        assert response.text == '"Hello, Unknown!"'
        print("Name route without parameter test passed")

        # Test stream route
        response = requests.get(f'{url}/stream')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/event-stream'
        
        # Read first 5 SSE events
        chunks = []
        for line in response.iter_lines():
            if line.startswith(b'data: '):
                chunks.append(int(line.decode('utf-8').replace('data: ', '')))
                if len(chunks) == 5:
                    break
        
        assert len(chunks) == 5, f"Expected 5 chunks from stream route, got {len(chunks)}"
        assert chunks == [0, 1, 2, 3, 4], f"Expected first 5 numbers, got {chunks}"
        print("Stream route test passed")

        # Test POST data route
        data = {"key": "value"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{url}/post-data', json=data, headers=headers)
        assert response.status_code == 200
        assert response.json() == data
        print("POST data route test passed")

    finally:
        # Cleanup: delete the deployed project
        genezio_delete(deploy_result.project_id)
        print("Project deleted and cleanup completed")

    print("All tests passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_fastapi_python()
