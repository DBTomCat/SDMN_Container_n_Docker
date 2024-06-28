#!/usr/bin/env python

import os
import sys
import subprocess

def set_memory_limit(limit):

    path = f"/sys/fs/cgroup/memory/container_{os.getpid()}"
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, "memory.limit_in_bytes"), 'w') as f:
        f.write(str(limit * 1024**2))
    
    with open(os.path.join(path, "tasks"), 'w') as f:
        f.write(str(os.getpid()))


def run_container(hostname, rootfs, limit=False):

    print(f"Container started running with PID: {os.getpid()}")

    if limit:
        set_memory_limit(limit)
    
    command = ["unshare", "--uts", "--net", "--pid", "--mount", "--fork", 
               "chroot", rootfs, "/bin/bash", "-c",
               f"mount -t proc proc /proc; hostname {hostname}; exec bash"]
    subprocess.run(command, check=True)


def main():
    name = sys.argv[1]
    rootfs = "container" # Equal to filesystem directory
    if len(sys.argv) > 2:
        run_container(name, rootfs, limit=int(sys.argv[2]))
    else:
        run_container(name, rootfs)

if __name__ == "__main__":
    main()

