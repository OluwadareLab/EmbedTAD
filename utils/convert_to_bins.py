import pandas as pd

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"

ORGANISMS = ["GM12878", "CH12LX"]
CHROMOSOMES = [19, 18]
RESOLUTIONS = [5000, 10000]
CHR_SIZE_FILES = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
TAD_FILENAMES = ["EmbedTAD.bed", "ClusterTAD.bed", "HiCseg.bed",
                  "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
ALGORITHMS = ["EmbedTAD", "ClusterTAD", "HiCseg",
               "Spectral", "TopDom", "Armatus", "IC-Finder", "Caspian"]
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
FILENAME_PREFIXES = ["gm12878_combined", "ch12lx"]


def main():
    for organism, chr in zip(ORGANISMS, CHROMOSOMES):
        print(f"Organism: {organism}")
        for resol in RESOLUTIONS:
            res = "10K" if resol == 10000 else "5K"
            for tad_filename in TAD_FILENAMES:
                print(f"{tad_filename}")
                tad_file = f"{BASE_PATH}/resutls/comparison/{organism.lower()}/{res}/{tad_filename}"
                tads = pd.read_csv(tad_file, delimiter=",", header=None)
                tads = tads.div(resol).round(0).astype(int)
                output_file = f"{BASE_PATH}/resutls/comparison/tads/{organism.lower()}_{chr}_{resol}_{tad_filename}"
                tads.to_csv(output_file, sep="\t", header=False, index=False)

if __name__ == "__main__":
    main()
