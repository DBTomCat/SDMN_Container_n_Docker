# Problem 2

## Load an ubuntu image into the filesystem
Using ```filesystem.sh```, we download and extract a basic ubuntu 20.04 image into the desired directory.

```bash
#!/bin/bash
mkdir container
cd container
wget https://cdimage.ubuntu.com/ubuntu-base/releases/focal/release/ubuntu-base-20.04.1-base-amd64.tar.gz
tar -xzvf ubuntu-base-20.04.1-base-amd64.tar.gz
rm ubuntu-base-20.04.1-base-amd64.tar.gz
```

## Container Creation:
Simply, we should create container using unshare command. Afterward we mount filesystem and run bash.
- rootfs should be equal to filesystem directory.

```python
def run_container(hostname, rootfs, limit=False):

    print(f"Container started running with PID: {os.getpid()}")

    if limit:
        set_memory_limit(limit)
    
    command = ["unshare", "--uts", "--net", "--pid", "--mount", "--fork", 
               "chroot", rootfs, "/bin/bash", "-c",
               f"mount -t proc proc /proc; hostname {hostname}; exec bash"]
    subprocess.run(command, check=True)
```
## Limit memory usage
We should add a memory cgroup to the system cgroups, I used process PID to name the cgroup. then we set memory limit and process PID with modifying ```memory.limit_in_bytes``` and ```tasks``` files.

```python
def set_memory_limit(limit):

    path = f"/sys/fs/cgroup/memory/container_{os.getpid()}"
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, "memory.limit_in_bytes"), 'w') as f:
        f.write(str(limit * 1024**2))
    
    with open(os.path.join(path, "tasks"), 'w') as f:
        f.write(str(os.getpid()))
```

## Run the CLI
- If there is no filesystem from before, first we should run ```filesystem.sh``` to download and make an ubuntu filesystem.
    ```bash
    ./filesystem.sh
    ```
- Then, we run ```container_runtime.py``` to create the container and run the CLI inside the filesystem.
    ```bash
    sudo ./container_runtime.py <Memory_limit_in_MB>
    ```
    This neads admin privileges to modify the memory cgroups.
## Sample output

```bash
amirhak@ubuntu:~/Desktop/HW2/SDMN_Container_n_Docker/P2$ sudo ./container_runtime.py salam 32
root@salam:/# ps fax
    PID TTY      STAT   TIME COMMAND
      1 ?        S      0:00 bash
      6 ?        R+     0:00 ps fax
root@salam:/# 
```