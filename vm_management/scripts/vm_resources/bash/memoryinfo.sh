#!/bin/bash

# Function to convert value to human-readable format
unit() {
    value=$1

    integer=${value%.*}
    length=${#integer}

    if ((length > 6)); then
        gb=$(echo "scale=4; $value / 1024^2" | bc)
        rounded_value=$(echo "$gb" | awk '{printf "%.2f", $0}')
        echo "$rounded_value GB"

    elif ((length >= 4 && length <= 6)); then
        mb=$(echo "scale=4; $value / 1024" | bc)
        rounded_value=$(echo "$mb" | awk '{printf "%.2f", $0}')
        echo "$rounded_value MB"

    elif ((length < 4)); then
        rounded_value=$(echo "$gb" | awk '{printf "%.2f", $0}')
        echo "$rounded_value KB"
    fi
}


# Read "/proc/meminfo" file
mem_available=$(grep MemTotal /proc/meminfo | awk '{print $2}')
mem_free=$(grep MemFree /proc/meminfo | awk '{print $2}')
buffers=$(grep Buffers /proc/meminfo | awk '{print $2}')
cached=$(grep -w "Cached" /proc/meminfo | awk '{print $2}')
kr=$(grep KReclaimable /proc/meminfo | awk '{print $2}')
huge_page_size=$(grep Hugepagesize /proc/meminfo | awk '{print $2}')


# Calculate mem_used
mem_used=$((mem_available - mem_free - buffers - cached - kr - huge_page_size))

# Calculate percentage
percentage=$((mem_used * 100 / mem_available))

# Convert values to human-readable format
mem_used_human=$(unit $mem_used)
mem_available_human=$(unit "$mem_available")

# Print the dictionary string
echo "{'used': $mem_used_human, 'available': $mem_available_human, 'percentage': $percentage}"
