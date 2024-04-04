#!/bin/bash

# This script setup the virbr0 bridge. This bridge connects the host with each guest Virtual Machine
# It's a bridge between the external LAN with the virtual LAN.
# It's allow us internet connections trought the NAT protocol, Asign dynamic Ip directions, and more.
virsh net-define /etc/libvirt/qemu/networks/default.xml
sleep 1
virsh net-start default
