#!/bin/bash

source ./env/access.sh

ip_address=$1

ansible all -i "'"$ip_address"'," -m shell -a "apt-get install nginx -y" \
--private-key=$path_to_sshkey \
-u $vm_username 
