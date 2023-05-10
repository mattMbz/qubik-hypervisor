#!/bin/bash

# Get global variables
source ./env/globals.sh


if [ -z "$1" ]; then
  echo "You must provide the name of the host you want to delete as an argument"
  exit 1
fi

# Update the entry in the addresses.xml file
xmlstarlet ed -L -u "//ip[@hostname='$1']/@used" -v "False" $xml_address_file
xmlstarlet ed -L -u "//ip[@hostname='$1']/@hostname" -v "None" $xml_address_file

## END
