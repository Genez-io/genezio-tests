#!/usr/bin/python3

import subprocess

def run_npm_run_build():
    process = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)

def run_curl(url):
    if url == None:
        print("URL is None")
        return 1

    process = subprocess.run(['curl', url], capture_output=True, text=True)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout

def run_node_script(script, args=[]):
    run_script_command = ['node', script] + args
    process = subprocess.run(run_script_command, capture_output=True, text=True)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout
