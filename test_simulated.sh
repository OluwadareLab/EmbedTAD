#!/bin/bash

input_dir="/home/hc0783.unt.ad.unt.edu/workspace/data/hictoolscompare/Simulations/sim_hic_count_matrix"
output_dir="/home/hc0783.unt.ad.unt.edu/workspace/data/results/embedtad/sim_hic_40k"
resolution=40000
worker="CPU"
normalization="True"

files=(
    "simHiC_countMatrix_409060_10-26_18h51m10s.txt"
    "simHiC_countMatrix_409060_10-26_18h55m22s.txt"
    "simHiC_countMatrix_409060_10-26_18h59m16s.txt"
    "simHiC_countMatrix_409060_10-26_19h03m11s.txt"
    "simHiC_countMatrix_4noise_10-19_23h11m57s.txt"
    "simHiC_countMatrix_818120_10-26_18h51m55s.txt"
    "simHiC_countMatrix_818120_10-26_18h55m56s.txt"
    "simHiC_countMatrix_818120_10-26_18h59m56s.txt"
    "simHiC_countMatrix_818120_10-26_19h03m53s.txt"
    "simHiC_countMatrix_8noise_10-19_23h12m59s.txt"
    "simHiC_countMatrix_1227180_10-26_18h34m41s.txt"
    "simHiC_countMatrix_1227180_10-26_18h52m41s.txt"
    "simHiC_countMatrix_1227180_10-26_18h56m39s.txt"
    "simHiC_countMatrix_1227180_10-26_19h00m40s.txt"
    "simHiC_countMatrix_1227180_10-26_19h04m33s.txt"
    "simHiC_countMatrix_1636240_10-26_18h35m39s.txt"
    "simHiC_countMatrix_1636240_10-26_18h53m29s.txt"
    "simHiC_countMatrix_1636240_10-26_18h57m30s.txt"
    "simHiC_countMatrix_1636240_10-26_19h01m24s.txt"
    "simHiC_countMatrix_1636240_10-26_19h05m28s.txt"
    "simHiC_countMatrix_2045301_10-26_18h54m22s.txt"
    "simHiC_countMatrix_2045301_10-26_18h58m23s.txt"
    "simHiC_countMatrix_2045301_10-26_19h02m20s.txt"
    "simHiC_countMatrix_2045301_10-26_19h06m23s.txt"
    "simHiC_countMatrix_20noise_10-21_19h30m07s.txt"
)

log_file="${output_dir}/embedtad_sim.log"
echo "EmbedTAD Execution Log" > "$log_file"
echo "Start Time: $(date)" >> "$log_file"
echo "---------------------------------------" >> "$log_file"

total_start_time=$(date +%s)

# log_resources() {
#     cpu_memory=$(python3 -c "import psutil; print(psutil.Process().memory_info().rss / (1024 ** 2))")  # Memory in MB
#     echo "$(date) - CPU Memory Usage: ${cpu_memory} MB" >> "$log_file"
    
#     gpu_memory=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
#     echo "$(date) - GPU Memory Usage: ${gpu_memory} MB" >> "$log_file"
# }

# log_continuously() {
#     while true; do
#         log_resources
#         sleep 1
#     done
# }

# log_continuously &
# log_pid=$!

for file in "${files[@]}"; do
    input_file="${input_dir}/${file}"
    if [[ -f "$input_file" ]]; then
        echo "Processing $file..." | tee -a "$log_file"
        
        base_name="${file%.txt}"
        clean_name="${base_name#simHiC_countMatrix_}"
        output_file="${output_dir}/embedtad_${clean_name}"

        chr_start_time=$(date +%s)
        python3 embedtad.py \
            --input "$input_file" \
            --output "$output_file" \
            --resolution "$resolution" \
            --worker "$worker" \
            --normalization "$normalization" \
            >> "$log_file" 2>&1
        chr_end_time=$(date +%s)

        chr_elapsed_time=$((chr_end_time - chr_start_time))
        echo "$file completed in $chr_elapsed_time seconds." | tee -a "$log_file"
    else
        echo "Input file $file not found. Skipping." | tee -a "$log_file"
    fi
done

total_end_time=$(date +%s)
total_elapsed_time=$((total_end_time - total_start_time))

echo "---------------------------------------" >> "$log_file"
echo "Total elapsed time: $total_elapsed_time seconds" | tee -a "$log_file"
echo "End Time: $(date)" >> "$log_file"

kill $log_pid