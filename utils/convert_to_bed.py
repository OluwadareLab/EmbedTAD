INPUT_PATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/raw/"
ORGANISM = ["gm12878", "ch12lx"]
FILENAMES = [["cuda_gm12878_10000_chr19.bed", "cuda_gm12878_10000_chr3.bed",
              "cuda_gm12878_5000_chr19.bed", "cuda_gm12878_5000_chr3.bed"],
             ["cuda_ch12lx_10000_chr18.bed", "cuda_ch12lx_10000_chr2.bed",
              "cuda_ch12lx_5000_chr18.bed", "cuda_ch12lx_5000_chr2.bed"]]
OUTPUT_PATH = "/home/mohit/Documents/project/EmbedTAD/data/chip_sig/"
for org, filename in zip(ORGANISM, FILENAMES):
    for fn in filename:
        chr = fn.split('_')[-1].replace(".bed", "")
        with open(f"{INPUT_PATH}{org}/{fn}", "r") as infile:
            with open(f"{OUTPUT_PATH}{org}/{fn}", "w") as outfile:
                for line in infile:
                    columns = line.strip().split('\t')
                    selected_columns = [chr, columns[1], columns[3]]
                    output_line = '\t'.join(selected_columns) + '\n'
                    outfile.write(output_line)
