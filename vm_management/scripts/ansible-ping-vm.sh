#!/bin/bash

source ./env/access.sh

ip_address=$1
ansible all -i "'"$ip_address"'," \
-m ping \
--private-key=$path_to_sshkey \
-u root \
-e 'ansible_python_interpreter=/usr/bin/python3'