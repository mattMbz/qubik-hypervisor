#!/bin/bash

# Get global variables
source ./env/globals.sh


if [ -z "$1" ]; then
  echo "Debe proporcionar el nombre del host a eliminar como argumento"
  exit 1
fi

# Actualizar la entrada del archivo addresses.xml
xmlstarlet ed -L -u "//ip[@hostname='$1']/@used" -v "False" $xml_address_file
xmlstarlet ed -L -u "//ip[@hostname='$1']/@hostname" -v "None" $xml_address_file

## END
