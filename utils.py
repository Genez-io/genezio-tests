#!/usr/bin/python3

import subprocess

def run_wget(url):
    if url == None:
        print("You")
        return 1

    process = subprocess.run(['wget', url], capture_output=True, text=True)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode

def run_npm_build():
    process = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode

def run_node_script(script, args=[]):
    run_script_command = ['node', script] + args
    process = subprocess.run(run_script_command, capture_output=True, text=True)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout
