#!/usr/bin/python3

import os
from genezio import genezio_login, genezio_local
from utils import compare_files
from os.path import exists

def test_kotlin_srv_py_cli():
    print("Starting kotlin srv - py sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)


    os.chdir("./projects/kotlin-srv-python-client/server/")
    
    print("Deploying locally...")
    process = genezio_local()

    assert process != None, "genezio local returned None"
    
    os.chdir("../client/")

    print("Checking files...")
    assert exists("./sdk/remote.py") == True, "Remote python sdk not found"
    assert exists("./sdk/helloWorldService.py") == True, "Class python sdk not found"
    assert exists("./sdk/Point.py") == True, "Additional \"Point\" Class not found"

    assert compare_files("./helloWorldService.template", "./sdk/helloWorldService.py") == True, "Wrong class sdk content"
    assert compare_files("./Point.template", "./sdk/Point.py") == True, "Wrong Additional \"Point\" class  content"
    
    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_kotlin_srv_py_cli()
