#!/usr/bin/python3

import os
from genezio import genezio_logout, genezio_login, genezio_account, genezio_deploy, genezio_local

def test_unauthenticated():
    print("Starting unauthenticated test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    return_code, stderr, stdout = genezio_account()

    assert return_code == 0, "genezio account returned non-zero exit code"
    assert "You are logged in." in stdout, "genezio account returned wrong output"

    return_code, stderr, stdout = genezio_logout()

    assert return_code == 0, "genezio account returned non-zero exit code"
    assert "You are now logged out!" in stdout, "genezio account returned wrong output"
    
    return_code, stderr, stdout = genezio_account()
    assert return_code == 1, "genezio account returned non-zero exit code"
    assert "You are not logged in or your token is invalid. Please run `genezio login` before running this command." in stderr, "genezio account returned wrong output"

    os.chdir("./projects/hello-world/server/")
    deploy_result = genezio_deploy(False)
    assert deploy_result.return_code == 1, "genezio account returned non-zero exit code"
    assert "You are not logged in or your token is invalid. Please run `genezio login` before running this command." in deploy_result.stderr, "genezio account returned wrong output"

    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_unauthenticated()
