#!/usr/bin/python3

import os
from genezio import genezio_deploy, genezio_login, genezio_local
from os.path import exists

def test_python_sdk():
    print("Starting python sdk test...")
    token = os.environ.get('GENEZIO_TOKEN')

    genezio_login(token)

    os.chdir("./projects/python-sdk/server/")
    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    assert exists("../client/sdk/remote.py") == True, "Remote swift sdk not found"
    assert exists("../client/sdk/server.py") == True, "Class python sdk not found"
    
    remote_template = open("./remote-python-template", "r")
    remote_templat_content = remote_template.read()
    
    assert remote_templat_content == open("../client/sdk/remote.py", "r").read(), "Remote python sdk is not the same as the template"
    
    f = open("../client/sdk/server.py", "r")
    content = f.read()

    assert "from .remote import Remote" in content, "Wrong import statement"
    
    assert "def method(self):" in content, "Wrong exported method without parameters"
    assert 'return Server.remote.call("Server.method")' in content, "Wrong exported method without parameters"
    
    assert 'def methodWithoutParameters(self):' in content, "Wrong exported method with return type"
    assert 'return Server.remote.call("Server.methodWithoutParameters")' in content, "Wrong exported method with return type"
    
    assert 'def methodWithOneParameter(self, test1):' in content, "Wrong exported method with one parameter"
    assert 'return Server.remote.call("Server.methodWithOneParameter", test1)' in content, "Wrong exported method with one parameter"
    
    assert 'def methodWithMultipleParameters(self, test1, test2):' in content, "Wrong exported method with multiple parameters"
    assert 'return Server.remote.call("Server.methodWithMultipleParameters", test1, test2)' in content, "Wrong exported method with multiple parameters"
    
    os.chdir("../server/")

    process = genezio_local()

    assert exists("../client/sdk/remote.py") == True, "Remote python sdk not found"
    assert exists("../client/sdk/server.py") == True, "Class python sdk not found"
    
    assert remote_templat_content == open("../client/sdk/remote.py", "r").read(), "Remote python sdk is not the same as the template"

    f = open("../client/sdk/server.py", "r")
    content = f.read()

    assert "from .remote import Remote" in content, "Wrong import statement"
    
    assert "def method(self):" in content, "Wrong exported method without parameters"
    assert 'return Server.remote.call("Server.method")' in content, "Wrong exported method without parameters"
    
    assert 'def methodWithoutParameters(self):' in content, "Wrong exported method with return type"
    assert 'return Server.remote.call("Server.methodWithoutParameters")' in content, "Wrong exported method with return type"
    
    assert 'def methodWithOneParameter(self, test1):' in content, "Wrong exported method with one parameter"
    assert 'return Server.remote.call("Server.methodWithOneParameter", test1)' in content, "Wrong exported method with one parameter"
    
    assert 'def methodWithMultipleParameters(self, test1, test2):' in content, "Wrong exported method with multiple parameters"
    assert 'return Server.remote.call("Server.methodWithMultipleParameters", test1, test2)' in content, "Wrong exported method with multiple parameters"
    

    process.kill()
    print("Test passed!")



# Test order matters because the commands are having side effects.
if __name__ == '__main__':
    test_python_sdk()