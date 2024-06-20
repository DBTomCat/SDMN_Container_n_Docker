#!/bin/bash

# Ping router from node1
ip netns exec node1 ping -c 4 172.0.0.1

# Ping router from node2
ip netns exec node2 ping -c 4 172.0.0.1

# Ping router from node3
ip netns exec node3 ping -c 4 10.10.0.1

# Ping router from node4
ip netns exec node4 ping -c 4 10.10.0.1
