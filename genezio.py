#!/usr/bin/python3

import subprocess
import re
import socket
import time
import os
import random

# define a struct
class DeployResult:
    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, stdout)

        if (len(links) > 0):
            self.web_urls = [x[0] for x in links[:-1]]
            self.project_url = links[-1][0]

def genezio_deploy(deploy_frontend):
    genezio_deploy_command = ['genezio', 'deploy']

    if (deploy_frontend == True):
        genezio_deploy_command.append("--frontend")
    genezio_deploy_command.append("--logLevel")
    genezio_deploy_command.append("info")

    process = subprocess.run(genezio_deploy_command, capture_output=True, text=True)

    return DeployResult(process.returncode, process.stdout, process.stderr)

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
        genezio_login_command.append(class_type)

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

def genezio_account():
    genezio_account_command = ['genezio', 'account']

    process = subprocess.run(genezio_account_command, capture_output=True, text=True)

    return process.returncode, process.stderr, process.stdout

def genezio_local():
    port = random.randint(1024, 40000)
    genezio_local_command = ['genezio', 'local', "--port", str(port), "--logLevel", "info"]

    process = subprocess.Popen(genezio_local_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, close_fds=True)
    start = time.time()

    while True:
        process.poll()
        time.sleep(0.05)

        if process.returncode != None:
            process.kill()
            return process

        # Test if port 8083 is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_status = sock.connect_ex(('127.0.0.1', port))

        if port_status == 0:
            break
        
        end = time.time()
        if end - start > 60:
            process.kill()
            return process
    
    time.sleep(6)
    return process

