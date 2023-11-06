#!/usr/bin/python3

import subprocess
import os

# We are using shell=True on Windows for subprocess.run()
use_shell = os.name == 'nt'

def run_npm_run_build():
    npm_run_build_args = ['npm', 'run', 'build']

    npm_run_build_command = ' '.join(npm_run_build_args) if use_shell else npm_run_build_args
    process = subprocess.run(npm_run_build_command, capture_output=True, text=True, shell=use_shell)

def run_curl(url):
    if url == None:
        print("URL is None")
        return 1

    print("Running curl " + url)
    curl_args = ['curl', url]

    curl_command = ' '.join(curl_args) if use_shell else curl_args
    process = subprocess.run(curl_command, capture_output=True, text=True, shell=use_shell)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout

def run_node_script(script, args=[]):
    run_script_args = ['node', script] + args

    run_script_command = ' '.join(run_script_args) if use_shell else run_script_args
    process = subprocess.run(run_script_command, capture_output=True, text=True, shell=use_shell)

    print(process.stdout)
    print(process.stderr)
    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout

def run_script(args):
    run_script_command = ' '.join(args) if use_shell else args
    process = subprocess.run(run_script_command, capture_output=True, text=True, shell=use_shell)

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout

# function that compares 2 files and returns true if they are the same
# the function needs to ingnore line endings as '\n' and '\r\n' are the same
def compare_files(path1, path2):
    with open(path1, 'r') as file1:
        with open(path2, 'r') as file2:
            line1 = file1.readline()
            line2 = file2.readline()
            if line1.rstrip() != line2.rstrip():
                print(line1, line2)
                return False

    return True
