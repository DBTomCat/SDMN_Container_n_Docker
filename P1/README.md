# Problem 1

## **Topology Setup**

Below is a Bash script that creates the required topology that mentiend in question.

```bash
#!/bin/bash

# Create network namespaces
ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4
ip netns add router

# Create bridges in the root namespace
ip link add br1 type bridge
ip link add br2 type bridge

# Set up bridges
echo "Setting bridges up"
ip link set br1 up
ip link set br2 up

# Create veth pairs and assign them to namespaces
echo "Creating veth pairs"
ip link add veth-node1 type veth peer name veth-br11
ip link add veth-node2 type veth peer name veth-br12
ip link add veth-node3 type veth peer name veth-br23
ip link add veth-node4 type veth peer name veth-br24
ip link add veth-router1 type veth peer name veth-br1
ip link add veth-router2 type veth peer name veth-br2

ip link set veth-node1 netns node1
ip link set veth-node2 netns node2
ip link set veth-node3 netns node3
ip link set veth-node4 netns node4
ip link set veth-router1 netns router
ip link set veth-router2 netns router


# Set up
echo "Setting devices up"
ip netns exec node1 ip link set veth-node1 up
ip netns exec node2 ip link set veth-node2 up
ip netns exec node3 ip link set veth-node3 up
ip netns exec node4 ip link set veth-node4 up
ip netns exec router ip link set veth-router1 up
ip netns exec router ip link set veth-router2 up

ip link set veth-br1 up
ip link set veth-br2 up
ip link set veth-br11 up
ip link set veth-br12 up
ip link set veth-br23 up
ip link set veth-br24 up


# Connect veth pairs to bridges
echo "Connecting veth pairs to bridges"
ip link set veth-br11 master br1
ip link set veth-br12 master br1
ip link set veth-br23 master br2
ip link set veth-br24 master br2
ip link set veth-br1 master br1
ip link set veth-br2 master br2


# Assign IP addresses to veth interfaces
echo "Assigning IP"
ip netns exec node1 ip addr add 172.0.0.2/24 dev veth-node1
ip netns exec node2 ip addr add 172.0.0.3/24 dev veth-node2
ip netns exec node3 ip addr add 10.10.0.2/24 dev veth-node3
ip netns exec node4 ip addr add 10.10.0.3/24 dev veth-node4
ip netns exec router ip addr add 172.0.0.1/24 dev veth-router1
ip netns exec router ip addr add 10.10.0.1/24 dev veth-router2


# Enable IP forwarding in the router
echo "Enabling IP Forwarding"
ip netns exec router sysctl -w net.ipv4.ip_forward=1

# Set default Gateways
echo "Setting up default Gateways"
ip netns exec node1 ip route add default via 172.0.0.1
ip netns exec node2 ip route add default via 172.0.0.1
ip netns exec node3 ip route add default via 10.10.0.1
ip netns exec node4 ip route add default via 10.10.0.1

echo "Network topology setup completed."
```

Also, We need an script to remove namespaces and bridges we made so it doesn't cause networking problems.

```bash
#!/bin/bash

# clean-up
ip netns del node1
ip netns del node2
ip netns del node3
ip netns del node4
ip netns del router
ip link delete br1 type bridge
ip link delete br2 type bridge
```

## **Pinging**

To ping a device from specific netns the following command should be executed:

```bash
ip netns exec <node-ns-name> ping <destination-ip>
```
We should write an script so we can replace target node (namespace) with destitaion ip.
This script pings one node from another node as specified by the parameters:

```bash
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source-node> <destination-node>"
    exit 1
fi

SOURCE=$1
DEST=$2

# Get IP address of the destination node
DEST_IP=$(ip netns exec $DEST ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}')


# Ping the destination from the source
ip netns exec $SOURCE ping -c 4 $DEST_IP
```

## 1. **Routing without a Router:**
- Lets remove the router!
```bash
ip netns del router
```
- Without the router, static routes must be configured on the bridges in the root namespace.
- On `br1` namespace:
```bash
ip route add 10.10.0.0/24 dev br2
```
- On `br2` namespace:
```bash
ip route add 172.0.0.0/24 dev br1
```


## 2. **Routing between Namespaces on Different Servers:**
If namespaces are on different servers but can see each other on Layer 2, Same as last part we should add proper routing rules to the servers. on each side, routing to outside should be set to system physical ethernet and nearby namespaces should be routed to the bridge.
