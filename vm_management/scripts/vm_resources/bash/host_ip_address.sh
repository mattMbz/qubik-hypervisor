#!/bin/bash

# Use ip command to get network interface information
interface_info=$(ip -4 addr show dev enp0s3)

# Use grep and awk to extract the IPv4 address
ipv4_address=$(echo "$interface_info" | awk '/inet /{gsub(/\/.*/, ""); print $2}')

if [ $? -eq 0 ]; then
    # Print the IPv4 address
    echo "$ipv4_address"
else
    echo "Error when get IP address"
fi