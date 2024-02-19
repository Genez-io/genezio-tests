#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_script, compare_files
from os.path import exists

def test_kotlin_srv_dart_cli():
    print("Starting kotlin srv - dart sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)


    os.chdir("./projects/kotlin-srv-dart-client/server/")
    
    print("Deploying locally...")
    process = genezio_local()

    assert process != None, "genezio local returned None"
    
    os.chdir("../client/")

    print("Checking files...")
    assert exists("../client/sdk/remote.dart") == True, "Remote dart sdk not found"
    assert exists("../client/sdk/hello_world_service.dart") == True, "Class dart sdk not found"

    assert compare_files("./sdk/hello_world_service.dart", "./hello_world_service.template") == True, "Wrong class sdk content"
    
    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_kotlin_srv_dart_cli()
