#!/usr/bin/python3
import subprocess
import re
import socket
import time
import os

from utils import kill_process

# We are using shell=True on Windows for subprocess.run()
use_shell = os.name == 'nt'


# define a struct
class DeployResult:
    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, str(stdout))
        self.stdout_all_links = links
        links = [x for x in links if "genezio.com/docs" not in x[0]]

        if (len(links) > 0):
            self.web_urls = [x[0] for x in links[:-1]]
            self.project_url = links[-1][0]
            self.project_id = self.project_url.split("/")[-1]


def genezio_deploy(deploy_frontend, with_config="./genezio.yaml", args=[]):
    genezio_deploy_args = ['genezio', 'deploy', '--config', with_config]

    if (deploy_frontend == True):
        genezio_deploy_args.append("--frontend")
    genezio_deploy_args.append("--logLevel")
    genezio_deploy_args.append("info")

    for arg in args:
        genezio_deploy_args.append(arg)

    genezio_deploy_command = genezio_deploy_args if not use_shell else ' '.join(genezio_deploy_args)
    process = subprocess.run(genezio_deploy_command, text=True, shell=use_shell,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return DeployResult(process.returncode, process.stdout, process.stderr)


def genezio_login(auth_token):
    genezio_login_args = ['genezio', 'login']

    if (auth_token != None):
        genezio_login_args.append(auth_token)

    genezio_login_command = ' '.join(genezio_login_args) if use_shell else genezio_login_args
    process = subprocess.run(genezio_login_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')
    return process.returncode, process.stderr, process.stdout


def genezio_logout():
    genezio_logout_args = ['genezio', 'logout']

    genezio_logout_command = ' '.join(genezio_logout_args) if use_shell else genezio_logout_args
    process = subprocess.run(genezio_logout_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    return process.returncode, process.stderr, process.stdout


def genezio_add_class(class_path, class_type):
    genezio_add_args = ['genezio', 'addClass', class_path]

    if (class_type != None):
        genezio_add_args.append(class_type)

    genezio_add_class = ' '.join(genezio_add_args) if use_shell else genezio_add_args
    process = subprocess.run(genezio_add_class, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    return process.returncode, process.stderr, process.stdout


def genezio_list(identifier, details):
    genezio_list_args = ['genezio', 'list']

    if (identifier != None):
        genezio_list_args.append(identifier)

    if (details == True):
        genezio_list_args.append("--long-listed")

    genezio_list_command = ' '.join(genezio_list_args) if use_shell else genezio_list_args
    process = subprocess.run(genezio_list_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    return process.returncode, process.stderr, process.stdout


def genezio_delete(project_id):
    genezio_delete_args = ['genezio', 'delete', '-f', project_id]

    genezio_delete_command = ' '.join(genezio_delete_args) if use_shell else genezio_delete_args
    process = subprocess.run(genezio_delete_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    return process.returncode, process.stderr, process.stdout


def genezio_generate_sdk(language):
    genezio_generate_sdk_args = ['genezio', 'generateSdk', "-lang", language]

    genezio_generate_sdk_command = ' '.join(genezio_generate_sdk_args) if use_shell else genezio_generate_sdk_args
    process = subprocess.run(genezio_generate_sdk_command, capture_output=True, text=True, shell=use_shell,
                             encoding='utf-8')

    return process.returncode, process.stderr, process.stdout


def genezio_account():
    genezio_account_args = ['genezio', 'account']

    genezio_account_command = ' '.join(genezio_account_args) if use_shell else genezio_account_args
    process = subprocess.run(genezio_account_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')
    return process.returncode, process.stderr, process.stdout


def genezio_local(args=[]):
    port = 8083
    genezio_local_args = ['genezio', 'local', "--logLevel", "info"] + args

    # Define the file paths
    stdout_file = os.path.join("..", "stdout.txt")
    stderr_file = os.path.join("..", "stderr.txt")

    genezio_local_command = ' '.join(genezio_local_args) if use_shell else genezio_local_args
    with open(stdout_file, "wb") as out_logs, open(stderr_file, "wb") as out_err:
        process = subprocess.Popen(genezio_local_command, stdout=out_logs, stderr=out_err, text=True, close_fds=True,
                                   shell=use_shell, encoding='utf-8')
    start = time.time()

    while True:
        process.poll()
        time.sleep(0.05)

        if process.returncode != None:
            print("process exited with code: " + str(process.returncode))
            kill_process(process)
            with open(stdout_file, "r", encoding='utf-8') as f:
                stdout = f.read()
                print(stdout)
            with open(stderr_file, "r", encoding='utf-8') as f:
                stderr = f.read()
                print(stderr)
            return None

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_status = sock.connect_ex(('127.0.0.1', port))

        if port_status == 0:
            break

        end = time.time()
        if end - start > 60:
            print("Timeout while waiting for localhost.")
            kill_process(process)
            with open(stdout_file, "r", encoding='utf-8') as f:
                stdout = f.read()
                print(stdout)
            with open(stderr_file, "r", encoding='utf-8') as f:
                stderr = f.read()
                print(stderr)
            return None

    time.sleep(6)
    return process


def genezio_create(project_type, name, region, backend=None, frontend=None):
    command_args = ['genezio', 'create', project_type, '--name', name, '--region', region]

    if project_type == 'fullstack':
        if not backend or not frontend:
            raise ValueError("Both 'backend' and 'frontend' must be specified for fullstack projects.")
        command_args.extend(['--backend', backend, '--frontend', frontend])
    elif project_type == 'backend':
        command_args.extend(['--backend', backend])
    elif project_type == 'nextjs':
        command_args.append('--default')
    elif project_type in ['expressjs', 'nitrojs', 'serverless']:
        pass
    else:
        raise ValueError(f"Unsupported project type: {project_type}")

    command = ' '.join(command_args) if use_shell else command_args
    result = subprocess.run(command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    if result.returncode != 0:
        raise RuntimeError(f"Command failed with return code {result.returncode}: {result.stderr.strip()}")

    return result.returncode

