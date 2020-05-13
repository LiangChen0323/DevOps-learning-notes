#!/usr/bin/env python3.8

import subprocess
import os
import argparse

parser = argparse.ArgumentParser(
    "Take a port number, kill the process that listining on the port")
parser.add_argument("port_number", type=int, help="Please give a port number")

args = parser.parse_args()

port = args.port_number

try:
    proc_res = subprocess.run(
        ["lsof", "-n", f"-i4TCP:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print(f"No process is listening on the port {port}")
else:
    listening = None
    for line in proc_res.stdout.splitlines():
        if "LISTEN" in line.decode():
            listening = line
            break
        if listening:
            pid = int(listening.split()[1])
            os.kill(pid, 9)
            print(f"Killed process {pid}")
        else:
            print(f"NO process is listening on port {port}")
