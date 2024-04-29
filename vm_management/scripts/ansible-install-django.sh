#!/bin/bash

source ./env/access.sh

ip_address=$1

ansible all -i "'"$ip_address"'," \
--private-key=$path_to_sshkey \
-m apt \
-a "name=python3-pip state=present" \
-u $vm_username

ansible all -i "'"$ip_address"'," \
--private-key=$path_to_sshkey \
-m pip \
-u $vm_username \
-a "name=django==3.2.16 state=present"
