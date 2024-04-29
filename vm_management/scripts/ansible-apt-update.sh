#!/bin/bash

source ./env/access.sh

ip_address=$1

ansible all -i "'"$ip_address"'," \
-m apt \
--private-key=$path_to_sshkey \
-a "update_cache=yes" -u $vm_username
