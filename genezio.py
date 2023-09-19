#!/usr/bin/python3

import subprocess
import re
import socket
import time
import os
import random

# We are using shell=True on Windows for subprocess.run()
use_shell = os.name == 'nt'

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

def genezio_deploy(deploy_frontend, args=[]):
    genezio_deploy_args = ['genezio', 'deploy']

    if (deploy_frontend == True):
        genezio_deploy_args.append("--frontend")
    genezio_deploy_args.append("--logLevel")
    genezio_deploy_args.append("info")

    for arg in args:
        genezio_deploy_args.append(arg)

    genezio_deploy_command = ' '.join(genezio_deploy_args) if use_shell else genezio_deploy_args
    process = subprocess.run(genezio_deploy_command, capture_output=True, text=True, shell=use_shell)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return DeployResult(process.returncode, process.stdout, process.stderr)

def genezio_login(auth_token):
    genezio_login_args = ['genezio', 'login']

    if (auth_token != None):
        genezio_login_args.append(auth_token)

    genezio_login_command = ' '.join(genezio_login_args) if use_shell else genezio_login_args
    process = subprocess.run(genezio_login_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_logout():
    genezio_logout_args = ['genezio', 'logout']

    genezio_logout_command = ' '.join(genezio_logout_args) if use_shell else genezio_logout_args
    process = subprocess.run(genezio_logout_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_add_class(class_path, class_type):
    genezio_add_args = ['genezio', 'addClass', class_path]

    if (class_type != None):
        genezio_add_args.append(class_type)

    genezio_add_class = ' '.join(genezio_add_args) if use_shell else genezio_add_args
    process = subprocess.run(genezio_add_class, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_ls(identifier, details):
    genezio_ls_args = ['genezio', 'ls']

    if (identifier != None):
        genezio_ls_args.append(identifier)

    if (details == True):
        genezio_ls_args.append("--long-listed")

    genezio_ls_command = ' '.join(genezio_ls_args) if use_shell else genezio_ls_args
    process = subprocess.run(genezio_ls_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_delete(project_id):
    genezio_delete_args = ['genezio', 'delete', '-f', project_id]

    genezio_delete_command = ' '.join(genezio_delete_args) if use_shell else genezio_delete_args
    process = subprocess.run(genezio_delete_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_generate_sdk(language):
    genezio_generate_sdk_args = ['genezio', 'generateSdk', "-lang", language]

    genezio_generate_sdk_command = ' '.join(genezio_generate_sdk_args) if use_shell else genezio_generate_sdk_args
    process = subprocess.run(genezio_generate_sdk_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_account():
    genezio_account_args = ['genezio', 'account']

    genezio_account_command = ' '.join(genezio_account_args) if use_shell else genezio_account_args
    process = subprocess.run(genezio_account_command, capture_output=True, text=True, shell=use_shell)

    return process.returncode, process.stderr, process.stdout

def genezio_local(args=[]):
    port = 8083
    genezio_local_args = ['genezio', 'local', "--logLevel", "info"] + args

    genezio_local_command = ' '.join(genezio_local_args) if use_shell else genezio_local_args
    with open("../stdout.txt","wb") as out_logs, open("../stderr.txt","wb") as out_err:
        process = subprocess.Popen(genezio_local_command, stdout=out_logs, stderr=out_err, text=True, close_fds=True, shell=use_shell)
    start = time.time()

    while True:
        process.poll()
        time.sleep(0.05)

        if process.returncode != None:
            print("process exited with code: " + str(process.returncode))
            process.kill()
            with open("stdout.txt", "r") as f:
                stdout = f.read()
                print(stdout)
            with open("stderr.txt", "r") as f:
                stderr = f.read()
                print(stderr)
            print("genezio local stdout: " + process.stdout.read())
            print("genezio local stderr: " + process.stderr.read())
            return None

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_status = sock.connect_ex(('127.0.0.1', port))

        if port_status == 0:
            print("genezio local server is up")
            break
        end = time.time()
        if end - start > 60:
            print("Timeout while waiting for localhost.")
            process.kill()
            with open("stdout.txt", "r") as f:
                stdout = f.read()
                print(stdout)
            with open("stderr.txt", "r") as f:
                stderr = f.read()
                print(stderr)
            print("genezio local stdout: " + process.stdout.read())
            print("genezio local stderr: " + process.stderr.read())
            return None

    time.sleep(6)
    return process
