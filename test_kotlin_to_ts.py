#!/usr/bin/python3

import os
from genezio import genezio_login, genezio_local
from utils import compare_files
from os.path import exists

def test_kotlin_srv_ts_cli():
    print("Starting kotlin srv - ts sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)


    os.chdir("./projects/kotlin-srv-ts-client/server/")
    
    print("Deploying locally...")
    process = genezio_local()

    assert process != None, "genezio local returned None"
    
    os.chdir("../client/")

    print("Checking files...")
    assert exists("./sdk/remote.ts") == True, "Remote ts sdk not found"
    assert exists("./sdk/helloWorldService.sdk.ts") == True, "Class ts sdk not found"
    assert exists("./sdk/Point.ts") == True, "Additional \"Point\" Class not found"

    assert compare_files("./helloWorldService.template", "./sdk/helloWorldService.sdk.ts") == True, "Wrong class sdk content"
    assert compare_files("./Point.template", "./sdk/Point.ts") == True, "Wrong Additional \"Point\" class  content"
    
    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_kotlin_srv_ts_cli()
