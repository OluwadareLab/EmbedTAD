#!/bin/bash

log_file="embedtad_th17.log"
echo "EmbedTAD Execution Log" > "$log_file"
echo "Start Time: $(date)" >> "$log_file"
echo "---------------------------------------" >> "$log_file"

total_start_time=$(date +%s)

input_dir="/home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418"
output_dir="/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418"
resolutions=(10000)
worker="GPU"
normalization="True"

log_resources() {
    cpu_memory=$(python3 -c "import psutil; p = psutil.Process($python_pid); print(p.memory_info().rss / (1024 ** 2))")  # Memory in MB
    echo "$(date) - CPU Memory Usage: ${cpu_memory} MB" >> "$log_file"
    
    gpu_memory=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    echo "$(date) - GPU Memory Usage: ${gpu_memory} MB" >> "$log_file"
}

log_continuously() {
    while true; do
        log_resources
        sleep 10
    done
}

Start the total execution and logging
echo "Processing Mouse Cell" | tee -a "$log_file"
for resolution in "${resolutions[@]}"; do
    for chr in $(seq 1 1 19); do
        input_file="${input_dir}/th17_${resolution}_chr${chr}.txt"
        output_file="${output_dir}/th17_${resolution}_chr${chr}"

        if [[ -f "$input_file" ]]; then
            echo "Processing chromosome $chr..." | tee -a "$log_file"

            chr_start_time=$(date +%s)

            python3 embedtad.py \
                --input "$input_file" \
                --output "$output_file" \
                --resolution "$resolution" \
                --worker "$worker" \
                --normalization "$normalization" &
            python_pid=$!

            log_continuously &

            log_pid=$!

            wait $python_pid

            chr_end_time=$(date +%s)
            chr_elapsed_time=$((chr_end_time - chr_start_time))

            echo "Chromosome $chr completed in $chr_elapsed_time seconds." | tee -a "$log_file"
            kill $log_pid
        else
            echo "Input file $input_file not found. Skipping chromosome $chr." | tee -a "$log_file"
        fi
    done
done


total_end_time=$(date +%s)
total_elapsed_time=$((total_end_time - total_start_time))

echo "---------------------------------------" >> "$log_file"
echo "Total elapsed time: $total_elapsed_time seconds" | tee -a "$log_file"
echo "End Time: $(date)" >> "$log_file"