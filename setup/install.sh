#!/bin/bash

echo
echo "Installing Qubik Hypervisor - version 1.0 "
sleep 1
echo
echo "Please wait ..."
sleep 3

# Kind of virtualizer
type_intel=$(lscpu | grep VT-x)
type_amd=$(lscpu | grep AMD-v)

install() {
    if lscpu | grep -q "VT-x" || lscpu | grep -q "AMD-v"; then
        echo "This architecture supports virtualization:"
        echo $type_intel
        echo $type_amd

		packages_to_install=(
			'qemu-system-x86' 
			'libvirt-clients'
			'libvirt-daemon-system'
			'bridge-utils'
  			'libguestfs-tools'
  			'genisoimage'
  			'virtinst'
  			'libosinfo-bin'
  			'xmlstarlet'
			'libvirt-dev'
			'build-essential'
			'python3-dev'
			'python3-venv'
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

    else
        echo
        echo "Virtualization is not supported by this architecture."
        echo
        echo "Possible solutions:"
        echo
        echo "1. Check hardware compatibility: Ensure that your system's hardware supports virtualization."
        echo "   Review the specifications of your processor and motherboard to confirm whether it supports virtualization."
        echo
        echo "2. Enable virtualization in BIOS/UEFI: Access your computer's BIOS or UEFI settings and look" 
        echo "   for the option related to virtualization. This option might be named 'Virtualization Technology (VT-x)'"
        echo
        echo "3. Consult with the manufacturer: If you're still experiencing issues after following the above steps, consider" 
        echo "   reaching out to the manufacturer of your computer or motherboard for further assistance. They may provide"
        echo "   specific information regarding your hardware's compatibility with virtualization and how to address the issue."
    fi
}


## call function
install