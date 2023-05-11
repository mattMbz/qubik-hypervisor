#!/bin/bash

################################################################################
# File Name: rename-vm.sh
# Author: Matias Barboza
# Date Created: May 10th, 2023
# Description: Change our virtual machine name.
# Version: 0.1
################################################################################


# Execute the command and store the output in variables
vm_name=$(virsh list --all | grep $1 | awk '{print $2}')

# Check if the output is equal to '-'
if [ "$vm_name" = "$1" ]; then
    
    output=$(virsh list --all | grep $1 | awk '{print $1}')
    
    if [ "$output" = "-" ]; then
        #echo "The VM is powerred off"
        mv /etc/libvirt/qemu/"$1".xml /etc/libvirt/qemu/"$2".xml
    else
        echo "The VM is running, for rename first turn off"
    fi

else
    echo "The requested VM does not exist!"
fi


## END
