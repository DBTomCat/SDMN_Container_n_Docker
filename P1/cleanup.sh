#!/bin/bash

# clean-up
ip netns del node1
ip netns del node2
ip netns del node3
ip netns del node4
ip netns del router
ip link delete br1 type bridge
ip link delete br2 type bridge