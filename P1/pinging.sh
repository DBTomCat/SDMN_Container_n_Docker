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