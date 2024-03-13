#!/usr/bin/python3
import os
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete
from utils import run_script, kill_process


def test_dart():
    print("Starting dart sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')
    genezio_login(token)

    os.chdir("./projects/dart-test/server")
    run_script(["dart", "pub", "get"])
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    os.chdir("../client/")
    run_script(["dart", "pub", "get"])
    status, output = run_script(["dart", "run", "./main.dart"])

    print(output)
    assert "100Hello World12hello42true1 21 210 20100 200a1000 10001000 2000b10000 1000010000 10000a20 4020 40b30 6030 603 1 2 33 1 2 33 1 2 33 0 0 1 2 2 43 0 0 1 2 2 43 11 12 13 14 15 161 1 2" in output, "Wrong output from dart test"

    os.chdir("../server")
    output = ""
    process = genezio_local()

    assert process != None, "genezio local returned None"

    status, output = run_script(["dart", "run", "../client/main.dart"])

    print(output)
    assert "100Hello World12hello42true1 21 210 20100 200a1000 10001000 2000b10000 1000010000 10000a20 4020 40b30 6030 603 1 2 33 1 2 33 1 2 33 0 0 1 2 2 43 0 0 1 2 2 43 11 12 13 14 15 161 1 2" in output, "Wrong output from dart test"
    kill_process(process)

    print("Prepared to delete project...")
    genezio_delete(deploy_result.project_id)
    print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_dart()
