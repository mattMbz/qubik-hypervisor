#!/bin/bash

# Get global variables
source ./env/globals.sh

# Find the first available IP
new_ip=$(xmlstarlet sel -t -v '//ip[@used="False"]/@value' -n $xml_address_file | head -n1)

if [ -z "$new_ip" ]; then
  echo
  exit 1
fi

# Update the 'used' property to "True".
xmlstarlet ed -L -u "//ip[@value='$new_ip']/@used" -v "True" $xml_address_file

echo "$new_ip"

## END
