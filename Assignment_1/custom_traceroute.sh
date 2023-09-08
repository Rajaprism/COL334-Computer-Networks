#!/bin/bash

destination=$1

if [ -z "$destination" ]; then
    echo "Usage: $0 <destination>"
    exit 1
fi

max_hops=30

for ttl in $(seq 1 $max_hops); do
    ping_result=$(ping -c 1 -t $ttl $destination)
    echo "$ttl: $ping_result"
    
    if echo "$ping_result" | grep -q "Time to live exceeded"; then
        continue
    fi
    
    if echo "$ping_result" | grep -q "64 bytes from"; then
        echo "Traceroute completed"
        break
    fi
done

