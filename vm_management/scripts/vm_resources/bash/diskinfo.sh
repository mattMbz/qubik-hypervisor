#!/bin/bash

# Execute 'df' command and capture the output
output=$(df / -h)

# Extract the second line of the output
line=$(echo "$output" | awk 'NR==2')

# Split the line into values
read -r filesystem size used available percentage mount <<< "$line"

# Print the dictionary-like string
echo "{
    'used': $used,
    'available': $available,
    'percentage': $percentage,
    'mounted': $mount
}"
