#!/bin/bash

# Log file
log_file="embedtad_cpu.log"
echo "EmbedTAD Execution Log" > "$log_file"
echo "Start Time: $(date)" >> "$log_file"
echo "---------------------------------------" >> "$log_file"

# Start the total timer
total_start_time=$(date +%s)

# Directory paths
input_dir="/home/mohit/Documents/project/embed_tad/data/raw"
output_dir="/home/mohit/Documents/project/embed_tad/data/results/cpu"
resolutions=(5000 10000)
worker="CPU"
normalization="True"

# Function to log resources (CPU & GPU memory usage)
log_resources() {
    # Log CPU memory usage using `psutil` through Python
    cpu_memory=$(python3 -c "import psutil; p = psutil.Process($python_pid); print(p.memory_info().rss / (1024 ** 2))")  # Memory in MB
    echo "$(date) - CPU Memory Usage: ${cpu_memory} MB" >> "$log_file"
    
    # Log GPU memory usage using `nvidia-smi`
    gpu_memory=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    echo "$(date) - GPU Memory Usage: ${gpu_memory} MB" >> "$log_file"
}

# Function to continuously log memory usage every second in the background
log_continuously() {
    while true; do
        log_resources
        sleep 10  # Log every 1 second
    done
}

Start the total execution and logging
echo "Processing GM12878" | tee -a "$log_file"
for resolution in "${resolutions[@]}"; do
    for chr in $(seq 1 1 22); do
        input_file="${input_dir}/gm12878/gm12878_${resolution}_chr${chr}.txt"
        output_file="${output_dir}/gm12878_${resolution}_chr${chr}"

        # Check if the input file exists
        if [[ -f "$input_file" ]]; then
            echo "Processing chromosome $chr..." | tee -a "$log_file"

            # Start the timer for this chromosome
            chr_start_time=$(date +%s)

            # Run the command and redirect both stdout and stderr to the log file
            python3 embedtad.py \
                --input "$input_file" \
                --output "$output_file" \
                --resolution "$resolution" \
                --worker "$worker" \
                --normalization "$normalization" &
            python_pid=$!  # Capture the PID of the Python process

            # Start the background process to log resources continuously
            log_continuously &

            # Get the PID of the background logging process
            log_pid=$!

            # Wait for the Python process to finish
            wait $python_pid

            # End the timer for this chromosome
            chr_end_time=$(date +%s)
            chr_elapsed_time=$((chr_end_time - chr_start_time))

            echo "Chromosome $chr completed in $chr_elapsed_time seconds." | tee -a "$log_file"

            # Kill the background logging process after the Python process finishes
            kill $log_pid
        else
            echo "Input file $input_file not found. Skipping chromosome $chr." | tee -a "$log_file"
        fi
    done
done

echo "Processing CH12.LX" | tee -a "$log_file"
for resolution in "${resolutions[@]}"; do
    for chr in $(seq 1 1 19); do
        input_file="${input_dir}/ch12lx/ch12lx_${resolution}_chr${chr}.txt"
        output_file="${output_dir}/ch12lx_${resolution}_chr${chr}"

        # Check if the input file exists
        if [[ -f "$input_file" ]]; then
            echo "Processing chromosome $chr..." | tee -a "$log_file"

            # Start the timer for this chromosome
            chr_start_time=$(date +%s)

            # Run the command and redirect both stdout and stderr to the log file
            python3 embedtad.py \
                --input "$input_file" \
                --output "$output_file" \
                --resolution "$resolution" \
                --worker "$worker" \
                --normalization "$normalization" &
            python_pid=$!  # Capture the PID of the Python process

            # Start the background process to log resources continuously
            log_continuously &

            # Get the PID of the background logging process
            log_pid=$!

            # Wait for the Python process to finish
            wait $python_pid

            # End the timer for this chromosome
            chr_end_time=$(date +%s)
            chr_elapsed_time=$((chr_end_time - chr_start_time))

            echo "Chromosome $chr completed in $chr_elapsed_time seconds." | tee -a "$log_file"

            # Kill the background logging process after the Python process finishes
            kill $log_pid
        else
            echo "Input file $input_file not found. Skipping chromosome $chr." | tee -a "$log_file"
        fi
    done
done

# End the total timer
total_end_time=$(date +%s)
total_elapsed_time=$((total_end_time - total_start_time))

echo "---------------------------------------" >> "$log_file"
echo "Total elapsed time: $total_elapsed_time seconds" | tee -a "$log_file"
echo "End Time: $(date)" >> "$log_file"