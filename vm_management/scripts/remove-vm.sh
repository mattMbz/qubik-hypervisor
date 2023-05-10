#!/bin/bash

# Global variables
source ./env/globals.sh

# Variable get a input parameter
vm_name=$1


# get IP and MAC address for VM that'll be deleted.
mac_address=$(xmlstarlet sel -t -v "//host[@name='$vm_name']/@mac" $xml_network_file)
ip_address=$(xmlstarlet sel -t -m "//host[@name='$vm_name']/@ip" -v . -n $xml_network_file)


# Delete and Unlink the virtual machine from the network
virsh net-update default delete ip-dhcp-host "<host mac='$mac_address' name='$vm_name' ip='$ip_address'/>" --live --config 
virsh undefine --remove-all-storage $vm_name
bash $remove_network_host $vm_name

## END
