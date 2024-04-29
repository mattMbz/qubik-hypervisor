#!/bin/bash

source ./env/access.sh

ip_address=$1

ansible all -i "'"$ip_address"'," \
--private-key=$path_to_sshkey \
-m shell \
-a "apt-get install nginx -y" \
-u $vm_username 
