#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete, genezio_create_project
from utils import kill_process


def initialize_test_environment():
    """
    Set up the environment for testing, including changing to the appropriate directory and logging in to genezio.
    """
    token = os.environ.get('GENEZIO_TOKEN')

    project_root = os.path.join(os.getcwd(), "projects", "create")
    os.makedirs(project_root, exist_ok=True)
    os.chdir(project_root)

    genezio_login(token)
    return project_root


def generate_project_variants():
    """
    Generate a list of all project configurations to be tested.
    """
    backend_variants = ["ts", "js"]
    frontend_variants = ["react-ts", "react-js", "vue-ts", "vue-js", "svelte-ts", "svelte-js"]
    project_types = ["fullstack", "backend", "nextjs", "expressjs", "nitrojs", "serverless"]

    projects = []

    for project_type in project_types:
        if project_type == "fullstack":
            for backend in backend_variants:
                for frontend in frontend_variants:
                    projects.append({
                        "type": project_type,
                        "name": f"test-{project_type}-{backend}-{frontend}",
                        "region": "us-east-1",
                        "backend": backend,
                        "frontend": frontend,
                        "test_local": True
                    })
        elif project_type == "backend":
            for backend in backend_variants:
                projects.append({
                    "type": project_type,
                    "name": f"test-{project_type}-{backend}",
                    "region": "us-east-1",
                    "backend": backend,
                    "test_local": True
                })
        elif project_type == "nextjs":
            projects.append({
                "type": project_type,
                "name": f"test-{project_type}",
                "region": "us-east-1",
                "test_local": False
            })
        else:
            projects.append({
                "type": project_type,
                "name": f"test-{project_type}",
                "region": "us-east-1",
                "test_local": True
            })

    return projects

def create_and_test_project(project):
    """
    Create, deploy, test locally, and then delete the project.

    :param project: A dictionary containing the project configuration.
    """
    project_name = project["name"]

    if os.path.exists(project_name):
        os.chmod(project_name, 0o777)
        os.remove(project_name)

    print(f"Creating project {project_name}...")

    try:
        create_project(project)
        os.chdir(project_name)
        deploy_result = genezio_deploy(False)

        assert deploy_result.return_code == 0, f"genezio deploy failed for {project_name}"
        assert deploy_result.project_url, f"genezio deploy returned empty project URL for {project_name}"

        if project["test_local"]:
            process_local = genezio_local()
            assert process_local, f"genezio local failed for {project_name}"
            kill_process(process_local)

        print(f"Deleting project {project_name}...")
        genezio_delete(deploy_result.project_id)
    finally:
        os.chdir("..")


def create_project(project):
    """
    Create a genezio project based on the provided configuration.

    :param project: A dictionary containing the project configuration.
    :raises ValueError: If required parameters are missing.
    """
    if project["type"] == "fullstack":
        create_result = genezio_create_project(
            project_type=project["type"],
            name=project["name"],
            region=project["region"],
            backend=project["backend"],
            frontend=project["frontend"]
        )
    elif project["type"] == "backend":
        create_result = genezio_create_project(
            project_type=project["type"],
            name=project["name"],
            region=project["region"],
            backend=project["backend"]
        )
    else:
        create_result = genezio_create_project(
            project_type=project["type"],
            name=project["name"],
            region=project["region"]
        )

    assert create_result == 0, f"genezio create {project['type']} failed for {project['name']}"


def test_genezio_create():
    """
    Main function to test genezio project creation, deployment, local testing, and deletion.
    """
    print("Starting genezio create test...")
    project_root = initialize_test_environment()
    projects_to_test = generate_project_variants()

    for project in projects_to_test:
        create_and_test_project(project)

    print("All tests passed!")


if __name__ == '__main__':
    test_genezio_create()
