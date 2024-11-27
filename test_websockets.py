#!/usr/bin/python3

import os

from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete
from utils import run_node_script, kill_process
from websocket import create_connection


def test_wesockets():
    print("Starting websockets test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/websocket/")

    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"
    assert len(deploy_result.web_urls) == 1, "incorrect number of web urls exported"

    print(deploy_result.web_urls)
    http_url = deploy_result.web_urls[0]
    wss_url = http_url.replace("https://", "wss://")
    print(wss_url)
    websocket = create_connection(wss_url)

    try:
        # Check welcome message
        welcome_message = websocket.recv()
        assert welcome_message == "Welcome to the WebSocket server!", "Incorrect welcome message"

        # Send a test message
        test_message = "Hello, WebSocket!"
        websocket.send(test_message)

        # Receive and validate the echo response
        response = websocket.recv()
        assert response == f"Echo: {test_message}", "Incorrect echo response"
        print("Received echo response:", response)

    finally:
        # Close the WebSocket connection
        websocket.close()

test_wesockets()
