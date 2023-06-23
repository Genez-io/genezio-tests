#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import run_script

def test_kotlin():
    print("Starting kotlin sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/kotlin-test/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")
    status, output = run_script(["./gradlew", "--quiet", "run"])

    print(output)
    assert "[Point(x=0, y=0), Point(x=1, y=2), Point(x=2, y=4), Point(x=3, y=6), Point(x=4, y=8), Point(x=5, y=10)]" in output, "Wrong output from kotlin test"

    output = ""
    os.chdir("../server/")
    process = genezio_local()

    assert process != None, "genezio local returned None"
    
    os.chdir("../client/")
    status, output = run_script(["./gradlew", "--quiet", "run"])

    print(output)
    assert "[Point(x=0, y=0), Point(x=1, y=2), Point(x=2, y=4), Point(x=3, y=6), Point(x=4, y=8), Point(x=5, y=10)]" in output, "Wrong output from kotlin test"
    process.kill()
    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_kotlin()
