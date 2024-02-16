#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_node_script, kill_process

def test_runtime_linux_webhooks():
    print("Starting webhook linux runtime test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/webhook/server/")

    deploy_result = genezio_deploy(False, "./genezio-runtime-linux.yaml")

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"
    assert len(deploy_result.web_urls) == 4, "incorrect number of web urls exported"

    os.chdir("../client/")

    status, output = run_node_script("test-webhook-example.js", deploy_result.web_urls)

    components = output.split("\n")
    assert components[0] == "Ok", "Component 0 returned wrong output"
    assert components[1] == 'text in body', "Component 1 returned wrong output"
    assert components[2] == "{ name: 'John' }", "Component 2 returned wrong output"
    assert components[3] == "contents of file", "Component 3 returned wrong output"

    os.chdir("../server/")

    process = genezio_local()

    assert process != None, "genezio local returned None"

    os.chdir("../client/")

    status, output = run_node_script("test-webhook-example.js", deploy_result.web_urls)

    components = output.split("\n")
    assert components[0] == "Ok", "Component 0 returned wrong output"
    assert components[1] == 'text in body', "Component 1 returned wrong output"
    assert components[2] == "{ name: 'John' }", "Component 2 returned wrong output"
    assert components[3] == "contents of file", "Component 3 returned wrong output"
    kill_process(process)

    os.chdir("../")
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_runtime_linux_webhooks()
