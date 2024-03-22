#!/bin/bash

echo
echo "Installing Qubik Hypervisor - version 1.0 "
sleep 2
echo
echo "Please wait ..."
sleep 2

packages_to_install=(
	'qemu-system-x86' 
	'libvirt-clients' 
	'libvirt-daemon-system'
	'bridge-utils'
  	'libguestfs-tools'
  	'genisoimage'
  	'virtinst'
	'nano'
  	'libosinfo-bin'
  	'xmlstarlet'
)

echo
echo
echo "The follow packges will be installed:"
echo

for package in "${packages_to_install[@]}"; do
	echo "$package"
done

sleep 2
echo

failed=()

# Start setup simulation
for package in "${packages_to_install[@]}"; do
	simulation_result=$(sudo apt-get install --no-install-recommends --dry-run $package 2>&1)

	# Check the output command
	if [ $? -eq 0 ]; then
  		echo -e "\e[32m$package ..... OK\e[0m"
	else
  		echo -e "\e[31m== ERROR =====================\e[0m"
  		echo -e "\e[31mError durante la instalación del paquete '$package'\e[0m"
  		echo -e "\e[31m$simulation_result\e[0m"
 		echo -e "\e[31m=============================\e[0m"
		failed+=" $package"
	fi
done


if [ ${#failed[@]} -gt 0 ]; then
	echo -e "\e[33mWARNING\e[0m"
	echo -e "\e[33mSome packages have failed. The installation cannot be completed!\e[0m"
	echo -e "\e[33mPlease, try again!\e[0m"
else
	echo
	for package in "${packages_to_install[@]}"; do
		echo -e "\e[32mInstalling '$package'\e[0m"
		sudo apt-get install -y $package
	done
	echo -e "\e[32mQubik Hypervisor has been installed Successfully!\e[0m"
fi

