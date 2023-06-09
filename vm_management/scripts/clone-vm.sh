#!/bin/bash

## Loading all global variables: files and directories
source ./env/globals.sh

# check if parameters are received correctly
# two parematers are mandatory
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <base_machine> <new_virtual_machine>"
    exit 1
fi

# The base machine name and the new machine name are received as parameters and stored in variables
base_machine=$1
new_virtual_machine=$2

# Clone virtual machine
virt-clone --original $base_machine --name $new_virtual_machine --auto-clone

# Check if virt-clone executed seccesfully
if [[ $? -ne 0 ]]; then
    echo "virt-clone failed"
    exit 1
fi

# Assign the new VM to a Network
# One script for add new host in the network is loaded in add_network_host global variable.
bash $add_network_host $new_virtual_machine

## END

