#!/usr/bin/python3

import subprocess
import platform

def set_shell():
    if platform.system() == "Windows":
        return True
    else:
        return False

def run_npm_run_build():
    shell = set_shell()
    process = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True, shell=shell)

    return process.returncode, process.stdout

def run_curl(url):
    if url == None:
        print("URL is None")
        return 1

    print("Running curl " + url)
    shell = set_shell()
    process = subprocess.run(['curl', url], capture_output=True, text=True, shell=shell)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout

def run_node_script(script, args=[]):
    run_script_command = ['node', script] + args
    shell = set_shell()
    process = subprocess.run(run_script_command, capture_output=True, text=True, shell=shell)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout
