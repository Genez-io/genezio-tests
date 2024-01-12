#!/usr/bin/python3

import os
from genezio import genezio_login, genezio_add_class
from utils import compare_files

GENEZIO_YAML_CONTENT = """name: test-new-project
region: us-east-1
cloudProvider: genezio
packageManager: npm
sdk:
  language: ts
  path: ./sdk/
classes: []
"""

def test_genezio_misc_cmds():
    print("Starting genezio misc test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    working_dir = os.path.join("projects", "new_project")

    os.chdir(working_dir)

    # Create a file named `genezio.yaml`
    with open("genezio.yaml", "w") as f:
        f.write(GENEZIO_YAML_CONTENT)

    returnCode, _, stdout = genezio_add_class("test-jsonrpc.js", None)
    assert returnCode == 0, "`genezio addClass test-jsonrpc.js` returned non-zero exit code"
    assert "Class added successfully" in stdout, "`genezio addClass test-jsonrpc.js` returned wrong output"

    returnCode, _, stdout = genezio_add_class("test-http.js", "http")
    assert returnCode == 0, "`genezio addClass test-http.js` returned non-zero exit code"
    assert "Class added successfully" in stdout, "`genezio addClass test-http.js` returned wrong output"

    assert compare_files("./genezio.yaml", "./genezio.yaml.template") == True, "genezio.yaml doesn't match genezio.yaml.template"

    assert os.path.exists("./test-jsonrpc.js"), "class file test-jsonrpc.js doesn't exist"
    assert os.path.exists("./test-http.js"), "class file test-http.js doesn't exist"

    returnCode, stderr, _ = genezio_add_class("test-jsonrpc.js", None)
    assert stderr[:-1] == "Class already exists.", "genezio add duplicated class returned wrong output: " + stderr[:-1]

    # cleanup
    os.unlink("./test-jsonrpc.js")
    os.unlink("./test-http.js")
    os.unlink("./genezio.yaml")

    print("Test passed!")

# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_genezio_misc_cmds()
