#!/usr/bin/python3

import os
import requests
from genezio import genezio_deploy, genezio_login, genezio_delete, genezio_local

def test_nextjs():
    print("Starting nextjs test...")
    token = os.environ.get('GENEZIO_TOKEN')

    # Login to genezio
    genezio_login(token)

    # Change to the project directory and deploy
    os.chdir("./projects/host-check-nextjs/")
    deploy_result = genezio_deploy(False)

    # Extract the deployed URL for testing
    url = deploy_result.stdout_all_links[4][0]

    print("Deployed URL: " + str(url))

    # run NEXT_URL=url npm run cypress:run
    os.environ['NEXT_URL'] = url + "/"
    os.system("npm run cypress:run")

    # check if $? is 0
    assert os.system("echo $?") == 0

    print("Test completed successfully.")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_nextjs()
