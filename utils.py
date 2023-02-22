#!/usr/bin/python3

import subprocess

def run_node_script(script, args=[]):
    run_script_command = ['node', script] + args
    process = subprocess.run(run_script_command, capture_output=True, text=True)

    return process.returncode, process.stdout
