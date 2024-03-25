#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_create, genezio_delete
from utils import kill_process


def test_genezio_create():
    print("Starting genezio create test...")
    token = os.environ.get('GENEZIO_TOKEN')

    os.chdir(os.path.join(os.getcwd(), "projects"))

    if not os.path.exists("create"):
        os.makedirs("create")

    os.chdir("create")

    genezio_login(token)

    backendVariants = ["ts", "js"]
    frontendVariants = ["react-ts", "react-js", "vue-ts", "vue-js", "svelte-ts", "svelte-js"]

    to_create = []

    for backend in backendVariants:
        for frontend in frontendVariants:
            to_create.append({"name": "test-" + backend + "-" + frontend, "region": "us-east-1", "backend": backend,
                              "frontend": frontend})

    for project in to_create:

        if os.path.exists(project["name"]):
            os.chmod(project["name"], 0o777)
            os.remove(project["name"])
        print("Creating project " + project["name"] + "...")
        create_result = genezio_create(project["name"], project["region"], project["backend"], project["frontend"])
        assert create_result == 0, "genezio create returned non-zero exit code"

        os.chdir(project["name"])
        deploy_result = genezio_deploy(False)

        assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
        assert deploy_result.project_url != "", "genezio deploy returned empty project url"

        process_local = genezio_local()
        assert process_local is not None, "genezio local returned None"

        kill_process(process_local)
        print("Prepared to delete project " + project["name"] + "...")
        genezio_delete(deploy_result.project_id)
        print(project["name"] + " test passed!")

        os.chdir("..")

    print("Test passed!")

if __name__ == '__main__':
    test_genezio_create()
