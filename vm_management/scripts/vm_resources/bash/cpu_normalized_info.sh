#!/bin/bash

declare -A time1_array
declare -A time2_array
declare -A percentage_array

#Read CPU cores
get_cores() {
    cores=$(cat /proc/cpuinfo | grep processor | wc -l)
    echo $cores
}

#Read CPU times from /proc/stat file
read_cpu_times() {
    cores=$(get_cores)

    for ((number=0; number<cores; number++)); do
        cpun="cpu$number"
        cpu_times=$(grep $cpun /proc/stat)
        echo $cpu_times
    done
}

#Extract time data only of cpu0, cpu1, cpu2 ... depend of $1 parameter
create_time_arrays() {
    while IFS= read -r line; do
        echo $line | grep $1
    done <<< $2
}

# NOTE # # # #
# According to several statistical analyzes carried out on the behavior of this VCPU, the conclusion was obtained that below
# 20% of use of this VPCU will be considered as idle. Therefore, in this function, the number is received as a parameter and 
# the threshold is compared with the value number. If the threshold is greater than to number, the awk command is used to 
# remove the integer part of the number and get only the decimal part. If the threshold is less than os equal to number, the 
# number is not changed. Then, the number transformed or not, is printed using the echo command.
# # # # # # # 

normalize() {
    number=$1
    threshold=20

    if (( $(echo "$number < $threshold" | bc -l) )); then
        # Remove the integer part of the number and keep only the decimal part
        normalized_number=$(echo "$number" | awk -F'.' '{print "0."$2}')
    else
        normalized_number=$number
    fi

    echo "$normalized_number"
}

cpu_times=$(read_cpu_times)

cpu_cores=$(get_cores)

for ((i=0; i<cpu_cores; i++)); do
   time1_array["cpu$i"]=$(create_time_arrays "cpu$i" "$cpu_times")
done

sleep 1

cpu_times=$(read_cpu_times)

for ((i=0; i<cpu_cores; i++)); do
   time2_array["cpu$i"]=$(create_time_arrays "cpu$i" "$cpu_times")
done


### Calculate times
for key in "${!time1_array[@]}"; do

    #Time 1
    line_1="${time1_array[$key]}"
    system_t1=$(echo $line_1 | awk '{print $4}')
    idle_t1=$(echo $line_1 | awk '{print $5}')

    #Time 2
    line="${time2_array[$key]}"
    system_t2=$(echo $line | awk '{print $4}')
    idle_t2=$(echo $line | awk '{print $5}')

    #CPU time calculation
    delta_idle_cpu=$((idle_t2 - idle_t1))
    delta_system_cpu=$((system_t2 - system_t1))
    cpu_total_time=$((delta_idle_cpu + delta_system_cpu))
    proportion_time=$(echo "scale=4; $delta_idle_cpu / $cpu_total_time" | bc)
    cpu_percentage=$(echo "scale=2; (1 - $proportion_time) * 100" | bc)

    # Format to two decimal places and add zero if less than zero
    formatted=$(awk -v val="$cpu_percentage" 'BEGIN{ printf "%.2f", val+0 }')
    #echo "$key $formatted %"

    percentage_array[$key]=$(normalize "$formatted")
done

## We build a python dictionary in String format with cpu data to be sent via sockets to a python client
## build a python dictionary in String format
dict_string="{ "

## Loop through the array and add the key-value pairs to the dictionary string
for key in "${!percentage_array[@]}"; do
    dict_string+="'$key':${percentage_array[$key]}, "
done

## Remove the extra comma at the end of the thread
dict_string=${dict_string%, }

## close the dictionary
dict_string+=" }"

## Print the dictionary string to be fetched from a socket server script
echo "$dict_string"

### END
