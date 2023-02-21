#!/usr/bin/python3

import subprocess
import re
import socket
import time

def genezio_deploy(deploy_frontend):
    genezio_deploy_command = ['genezio', 'deploy']

    if (deploy_frontend == True):
        genezio_deploy_command.append("--frontend")
    genezio_deploy_command.append("--logLevel")
    genezio_deploy_command.append("info")

    process = subprocess.run(genezio_deploy_command, capture_output=True, text=True)

    m = re.match(r'Deploying your project to genezio infrastructure\.\.\..*Generating your SDK\.\.\..*Generating your SDK\.\.\..*Checking your credentials\.\.\..*Your project has been deployed and is available at ([a-zA-Z:\/.0-9-]*)', str(process.stdout).replace("\n", ""), re.DOTALL)

    return process.returncode, m.group(1)

def genezio_login(auth_token):
    genezio_login_command = ['genezio', 'login']

    if (auth_token != None):
        genezio_login_command.append(auth_token)

    process = subprocess.run(genezio_login_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_logout():
    genezio_logout_command = ['genezio', 'logout']

    process = subprocess.run(genezio_logout_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_add_class(class_path, class_type):
    genezio_login_command = ['genezio', 'addClass', class_path]

    if (class_type != None):
        genezio_deploy_command.append(class_type)

    process = subprocess.run(genezio_login_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_ls(identifier, details):
    genezio_ls_command = ['genezio', 'ls']

    if (identifier != None):
        genezio_ls_command.append(identifier)

    if (details == True):
        genezio_ls_command.append("--long-listed")

    process = subprocess.run(genezio_ls_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_delete(project_id):
    genezio_delete_command = ['genezio', 'delete', '-f', project_id]

    process = subprocess.run(genezio_delete_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_generate_sdk(language):
    genezio_generate_sdk_command = ['genezio', 'generateSdk', "-lang", language]

    process = subprocess.run(genezio_generate_sdk_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_local():
    genezio_local_command = ['genezio', 'local', "--logLevel", "info"]

    process = subprocess.Popen(genezio_local_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    start = time.time()

    while True:
        time.sleep(0.05)
        # Test if port 8083 is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_status = sock.connect_ex(('127.0.0.1',8083))

        if port_status == 0:
            break
        
        end = time.time()
        if end - start > 60:
            assert false, "Connecting to port 8083 failed"
    
    time.sleep(2)
