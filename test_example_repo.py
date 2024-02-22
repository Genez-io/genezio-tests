#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from utils import kill_process


def test_example_repo(language: str, repoNameExample: str, path: str):
	print("Starting {} test...".format(language + " " + repoNameExample))
	token = os.environ.get('GENEZIO_TOKEN')

	os.chdir(os.path.join(path, "projects", "examples", "genezio-examples", language, repoNameExample))

	genezio_login(token)

	deploy_result = genezio_deploy(False)

	assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
	assert deploy_result.project_url != "", "genezio deploy returned empty project url"

	process = genezio_local()

	assert process != None, "genezio local returned None"
	kill_process(process)
	print("Test passed!")


# Test order matters because the commands are having side effects.
if __name__ == '__main__':
	test_example_repo("typescript", "webhook", os.getcwd())
