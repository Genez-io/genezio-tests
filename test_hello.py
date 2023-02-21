#!/usr/bin/python3

import os
import requests
import test as gnz_test
from genezio import genezio_deploy, genezio_login
from utils import run_node_script

NODE_FILENAME = "../client/test-hello-sdk.js"

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    print("Starting hello_world for Javascript test...")

    genezio_login("735614a4514b93b523fd90cd2342d2ed013ccf6ba38b90bea6fcc6c36a23942d775d83bb03c5539441e28fab8bd6c9acdbdde4c64bb3360bf6cfcda891d2b68f")

    os.chdir("./projects/hello-world/server/")
    status, project_url = genezio_deploy(False)

    assert status == 0, "genezio deploy returned non-zero exit code"
    assert project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")

    status, output = run_node_script("test-hello-sdk.js")

    assert status == 0, "Node script returned non-zero exit code"

    components = output.split("\n")
    
    assert components[0] == "Hello world!", "Node script returned wrong output"
    assert components[1] == "Hello, George, from Tenerife!", "Node script returned wrong output"

    print("Test passed!")

