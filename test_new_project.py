#!/usr/bin/python3

import os
from genezio import genezio_login, genezio_init, genezio_add_class

def test_new_project():
    print("Starting new_project test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    working_dir = os.path.join("projects", "new_project")
    
    os.chdir(working_dir)
    
    genezio_init("test-new-project")
    
    genezio_add_class("test-jsonrpc.js", None)
    genezio_add_class("test-http.js", "http")
    
    genezio_yaml = open("./genezio.yaml", "r").read()
    
    genezio_yaml_template = open("./genezio.yaml.template", "r").read()
    
    assert genezio_yaml == genezio_yaml_template

    assert os.path.exists("./test-jsonrpc.js")
    assert os.path.exists("./test-http.js")
        
    returnCode, stderr, stdout = genezio_add_class("test-jsonrpc.js", None)

    assert stderr[:-1] == "Class already exists."
    
    
    print("Test passed!")
    

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_new_project()