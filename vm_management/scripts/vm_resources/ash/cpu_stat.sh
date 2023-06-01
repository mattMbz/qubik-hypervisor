#!/bin/ash

#Read CPU cores
get_cores() {
    cores=$(cat /proc/cpuinfo | grep processor | wc -l)
    echo $cores
}


#Read CPU times from /proc/stat file
read_cpu_times() {
    cores=$(get_cores)

    number=0
    while [ "$number" -lt "$cores" ]; do
        cpun="cpu$number"
        cpu_times=$(grep "$cpun" /proc/stat)
        echo "$cpu_times"
        number=$((number + 1))
    done
}


read_cpu_times
