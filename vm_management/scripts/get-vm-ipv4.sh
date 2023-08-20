#!/bin/bash

################################################################################
# File Name: get-vm-ipv4.sh
# Author: Matias Barboza
# Date Created: 
# Description: 
# Version: 
################################################################################

# Get global variables
source ./env/globals.sh

# Verifies that a hostname was supplied as a parameter
if [ $# -ne 1 ]; then
  echo "Uso: $0 <hostname>"
  exit 1
fi

# Hostname supplied as a parameter
hostname="$1"

# Use xmlstarlet to find the IP address based on the hostname
ip_address=$(xmlstarlet sel -t -v "//ip[@hostname='$hostname']/@value" $xml_address_file)

# Check if an IP address was found for the given hostname
if [ -n "$ip_address" ]; then
  echo "$ip_address"
else
  echo "not found"
fi