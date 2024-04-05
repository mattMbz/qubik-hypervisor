#!/bin/bash

# Load Global variables
source ./env/access.sh

ip_addr=$1

eval $(ssh-agent -s)
ssh-add $path_to_sshkey
sleep 1
sshpass -p $vm_user_password ssh-copy-id -i $path_to_sshkey $vm_username@$ip_addr
