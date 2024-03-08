#!/usr/bin/python3

import subprocess
import os
import difflib
import psutil
import signal

# We are using shell=True on Windows for subprocess.run()
use_shell = os.name == 'nt'


def run_npm_run_build():
    npm_run_build_args = ['npm', 'run', 'build']

    npm_run_build_command = ' '.join(npm_run_build_args) if use_shell else npm_run_build_args
    process = subprocess.run(npm_run_build_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')


def run_curl(url):
    if url == None:
        print("URL is None")
        return 1

    print("Running curl " + url)
    curl_args = ['curl', url]

    curl_command = ' '.join(curl_args) if use_shell else curl_args
    process = subprocess.run(curl_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout


def run_node_script(script, args=[]):
    run_script_args = ['node', script] + args

    run_script_command = ' '.join(run_script_args) if use_shell else run_script_args
    process = subprocess.run(run_script_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    print(process.stdout)
    print(process.stderr)
    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout


def run_script(args):
    run_script_command = ' '.join(args) if use_shell else args
    process = subprocess.run(run_script_command, capture_output=True, text=True, shell=use_shell, encoding='utf-8')

    if process.returncode != 0:
        print(process.stderr)
        print(process.stdout)

    return process.returncode, process.stdout


# function that compares 2 files and returns true if they are the same
# the function needs to ingnore line endings as '\n' and '\r\n' are the same
def compare_files(path1, path2):
    with open(path1, 'r', encoding='utf-8') as file1, open(path2, 'r', encoding='utf-8') as file2:
        # Read the contents of both files
        content1 = file1.read()
        content2 = file2.read()

        # Normalize line endings
        content1 = content1.replace('\r\n', '\n')
        content2 = content2.replace('\r\n', '\n')

        # Print a diff for debugging in case the files are different
        if (content1 != content2):
            diff = difflib.Differ().compare(content1.splitlines(True), content2.splitlines(True))
            print('Diff:\n')
            print(''.join(diff))

        # Compare the contents
        return content1 == content2


def kill_process(process: subprocess.Popen):
    if use_shell:
        try:
            parent = psutil.Process(process.pid)
        except psutil.NoSuchProcess:
            print(f"Kill of process with pid {process.pid} was requested, but this process does not exist")
            return

        children = parent.children(recursive=True)
        # Kill all children
        for child in children:
            child.kill()
            # Kill the process
        parent.kill()
    else:
        process.kill()
