#!/bin/bash

INTERVAL=1
LOG_FILE="memory_usage.log"
echo -e "Timestamp\t\tGPU Memory Used (MB)\tGPU Memory Free (MB)\tGPU Utilization (%)\tSystem Memory Used (MB)\tSystem Memory Available (MB)" >> "$LOG_FILE"
while true; do
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

    GPU_MEMORY_USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null)
    GPU_MEMORY_FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null)
    GPU_UTILIZATION=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null)

    RAM_USAGE=$(free -m | grep Mem | awk '{print $3}')
    RAM_AVAILABLE=$(free -m | grep Mem | awk '{print $7}')

    combined_var=$(printf "%-20s\t%-25s\t%-25s\t%-20s\t%-30s\t%-30s\n" "$TIMESTAMP" "$GPU_MEMORY_USED" "$GPU_MEMORY_FREE" "$GPU_UTILIZATION" "$RAM_USAGE" "$RAM_AVAILABLE")
    echo -e "$combined_var" >> "$LOG_FILE"

    sleep $INTERVAL
done