#!/bin/bash

# Load Global variables
# xml file paths

source ./env/globals.sh

# New values for the host.
vm_name=$1
mac_address=$(virsh dumpxml $1 | xmlstarlet sel -t -v "//mac/@address")
new_ip=$(bash $get_ip_address)

# Check if an available IP was found.
if [ -z "$new_ip" ]; then
  echo "There are no available IP addresses"
  exit 1
fi

# Add the new host to the XML file.
virsh net-update default add-last ip-dhcp-host "<host mac='$mac_address' name='$vm_name' ip='$new_ip' />" --live --config

# Add the variable 'new_name' to the 'hostname' property of the 'addresses.xml' file.
xmlstarlet ed -L -u "//ip[@value='$new_ip']/@hostname" -v "$vm_name" $xml_address_file

## END
