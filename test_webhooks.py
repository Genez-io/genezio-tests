#!/usr/bin/python3

import os
import requests
import test as gnz_test
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    print("Starting hello_world for Javascript test...")

    genezio_login("735614a4514b93b523fd90cd2342d2ed013ccf6ba38b90bea6fcc6c36a23942d775d83bb03c5539441e28fab8bd6c9acdbdde4c64bb3360bf6cfcda891d2b68f")

    os.chdir("./projects/webhook/server/")

    status, project_url, web_urls = genezio_deploy(False)

    assert status == 0, "genezio deploy returned non-zero exit code"
    assert project_url != "", "genezio deploy returned empty project url"
    assert len(web_urls) == 4, "incorrect number of web urls exported"

    os.chdir("../client/")

    status, output = run_node_script("test-webhook-example.js", web_urls)

    components = output.split("\n")
    assert components[0] == "Ok", "Component 0 returned wrong output"
    assert components[1] == 'text in body', "Component 1 returned wrong output"
    assert components[2] == "{ name: 'John' }", "Component 2 returned wrong output"
    assert components[3] == "contents of file", "Component 3 returned wrong output"

    print("Test passed!")
