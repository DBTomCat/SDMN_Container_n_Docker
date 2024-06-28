#!/bin/bash

mkdir container
cd container
wget https://cdimage.ubuntu.com/ubuntu-base/releases/focal/release/ubuntu-base-20.04.1-base-amd64.tar.gz
tar -xzvf ubuntu-base-20.04.1-base-amd64.tar.gz 
rm ubuntu-base-20.04.1-base-amd64.tar.gz