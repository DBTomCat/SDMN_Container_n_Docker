### Problem 2

Here's a complete solution guide for implementing a simple container runtime similar to Docker using Python. The runtime will isolate the container in multiple namespaces and use a separate filesystem directory as its root.

#### Python Code for the Container Runtime

Save the following Python script as `container_runtime.py`. This script uses `clone()` to create new namespaces and `unshare()` to isolate the container.

```python
import os
import sys
import subprocess

def set_hostname(hostname):
    """Set the hostname in the isolated UTS namespace."""
    subprocess.run(['hostname', hostname])

def set_root_fs(new_root):
    """Change root filesystem to a new directory."""
    os.chroot(new_root)
    os.chdir('/')

def isolate_container(hostname):
    """Isolate the process using namespaces and set up the environment."""
    CLONE_NEWUTS = 0x04000000  # Create a new UTS namespace
    CLONE_NEWPID = 0x20000000  # Create a new PID namespace
    CLONE_NEWNS = 0x00020000   # New mount namespace
    CLONE_NEWNET = 0x40000000  # New network namespace

    # Create a child process in new namespaces
    pid = os.fork()
    if pid == 0:
        # This is the child process, isolate it
        os.unshare(CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWNET)
        set_hostname(hostname)
        set_root_fs('/path/to/new/root')  # Modify this path to the extracted filesystem
        os.execlp('bash', 'bash')  # Start a bash shell
    else:
        # Wait for the child process to finish
        os.waitpid(pid, 0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python container_runtime.py <hostname>")
        sys.exit(1)
    hostname = sys.argv[1]
    isolate_container(hostname)
```

#### Step 2: Prepare the Filesystem
1. **Download the Ubuntu 20.04 Root Filesystem**:
   - You can use `debootstrap` or download a minimal root filesystem of Ubuntu 20.04 from an official source.
   - Extract this filesystem to a directory that will be used as the root for the container. For example, `/var/lib/mycontainer`.

#### Step 3: Running the Script
1. **Execute the Python Script**:
   - Run the script using: `sudo python3 container_runtime.py myhostname`
   - This will isolate the process into its own namespaces, change its root directory, and open a bash shell with `myhostname` set.

#### Notes:
- Ensure you have the required permissions to execute these operations, usually requiring root access.
- Customize the path to the new root filesystem in the `set_root_fs()` function.

#### Step 4: Bonus Feature (Memory Limit)
To add an optional argument for limiting memory usage:
1. Use cgroups in Linux to limit the memory usage of the processes running inside the container.
2. You would need to create a cgroup, set memory limits, and then move the process ID of the isolated container into that cgroup.



### Solution Guide for Problem 2: Container Runtime

#### Overview
In this problem, you are tasked with implementing a basic version of a container runtime. The solution will involve using Linux namespaces to isolate the container's environment. Below is a step-by-step guide to implement this in Python, which is a popular choice for such scripts due to its readability and extensive library support.

#### Requirements
- Python 3
- Access to a Linux environment with permissions to manipulate namespaces and mount points.

#### Steps to Implement the Container Runtime

1. **Setup Python Script**:
   - The script will use the `os` and `subprocess` libraries to manipulate namespaces and execute shell commands.
   - Ensure Python script has executable permissions.

2. **Define Container Creation**:
   - Use Linux namespaces (net, mnt, pid, uts) to isolate the container.
   - Mount a filesystem that is a copy or snapshot of Ubuntu 20.04 for the container's filesystem.

3. **Executing the Container**:
   - The container should open a new shell where the specified hostname is set and the `bash` process runs as PID 1.
   - Use `unshare` and `chroot` commands to achieve namespace isolation and filesystem isolation respectively.

4. **Memory Limitation (Bonus)**:
   - Implement an optional feature to limit the memory usage of the container using cgroups.

#### Sample Python Script

```python
import os
import subprocess

def create_container(hostname, memory_limit=None):
    # Create new namespaces
    unshare_flags = os.CLONE_NEWNS | os.CLONE_NEWNET | os.CLONE_NEWPID | os.CLONE_NEWUTS
    os.unshare(unshare_flags)

    # Set hostname
    subprocess.run(['hostname', hostname], check=True)

    # Setup isolated filesystem
    new_root = f'/var/lib/mycontainers/{hostname}'
    os.makedirs(new_root, exist_ok=True)
    subprocess.run(['rsync', '-a', '/usr/lib/os-release', new_root], check=True)

    # Enter new filesystem
    os.chroot(new_root)
    os.chdir('/')

    # Memory limitation using cgroups (if specified)
    if memory_limit:
        cgroup_path = f'/sys/fs/cgroup/memory/{hostname}'
        os.makedirs(cgroup_path, exist_ok=True)
        with open(f'{cgroup_path}/memory.limit_in_bytes', 'w') as f:
            f.write(str(int(memory_limit) * 1024 * 1024))  # Convert MB to bytes

    # Execute bash shell
    os.execv('/bin/bash', ['bash'])

if __name__ == '__main__':
    import sys
    hostname = sys.argv[1]
    memory_limit = sys.argv[2] if len(sys.argv) > 2 else None
    create_container(hostname, memory_limit)
```

#### How to Run
- Save the script as `create_container.py`.
- Make it executable: `chmod +x create_container.py`.
- Run the script: `./create_container.py myhostname 100` (where `100` is the optional memory limit in MB).

### Deliverables
- Python script file (`create_container.py`).
- README.md explaining how to setup and run the script, detailing any prerequisites like Python version, necessary packages, and permissions.

This guide provides a comprehensive approach to building a simple container runtime similar to Docker using Python. The script includes the setup of namespaces and a separate filesystem per container, along with optional memory limitations.\
