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
    # Extract the deployed URL for testing
    url = None
    for link in deploy_result.stdout_all_links:
        if "app.geneziodev.com" in link[0] or "next.genez.io" in link[0]:
            url = link[0]
            break

    # Add error handling for when URL is not found
    assert url is not None, "Could not find deployed nextjs URL in deployment output"
    print("Deployed URL: " + str(url))

    # create a new .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f"NEXT_URL={url}/\n")
    
    # Update cypress.config.ts with the correct URL
    with open('cypress.config.ts', 'r') as f:
        config_content = f.read()
    
    config_content = config_content.replace('"<NEXT_URL>"', f'"{url}"')
    
    with open('cypress.config.ts', 'w') as f:
        f.write(config_content)
    
    # Run Cypress tests and capture the return code
    cypress_result = os.system("npm run cypress:run")
    
    # Check if Cypress tests passed
    assert cypress_result == 0, "Cypress tests failed"

    genezio_delete(deploy_result.project_id)
    print("Test completed successfully.")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_nextjs()
