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
    
    os.system("npm install")
    
    print("Deploying...")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned a non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned an empty project URL"

    print("deploy_result.stdout_all_links: " + str(deploy_result.stdout_all_links))
    print("deploy_result.project_url: " + str(deploy_result.project_url))

    # Extract the deployed URL for testing
    url = deploy_result.stdout_all_links[4][0]

    print("Deployed URL: " + str(url))

    # run NEXT_URL=url npm run cypress:run
    os.environ['NEXT_URL'] = url + "/"
    # Run Cypress tests and capture the return code
    cypress_result = os.system("npm run cypress:run")
    
    # Check if Cypress tests passed
    assert cypress_result == 0, "Cypress tests failed"

    genezio_delete(deploy_result.project_id)
    print("Test completed successfully.")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_nextjs()
