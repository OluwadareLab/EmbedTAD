import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"

# ORGANISMS = ["GM12878", "CH12LX"]
# CHROMOSOMES = [19, 18]
# RESOLUTIONS = [5000, 10000]
# CHR_SIZE_FILES = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
# TAD_FILENAMES = ["EmbedTAD.bed", "ClusterTAD.bed", "HiCseg.bed",
#                   "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
# ALGORITHMS = ["EmbedTAD", "ClusterTAD", "HiCseg",
#                "Spectral", "TopDom", "Armatus", "IC-Finder", "Caspian"]
# COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#           '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# FILENAME_PREFIXES = ["gm12878_combined", "ch12lx"]

ORGANISMS = ["GM12878"]
CHROMOSOMES = [19]
RESOLUTIONS = [10000]
CHR_SIZE_FILES = ["hg19.chrom.sizes"]
TAD_FILENAMES = ["ClusterTAD.bed"]
ALGORITHMS = ["ClusterTAD"]
COLORS = ['#1f77b4']
FILENAME_PREFIXES = ["gm12878_combined"]

def get_cf(matrix: np.matrix, domains: pd.DataFrame, resol):
    count = len(domains)
    for i in range(0, count, 1):
        start = int(domains.iloc[i, 0]/resol)
        end = int(domains.iloc[i, 1]/resol)
        domains.iloc[i, 2] = np.trace(matrix[start:end+1, start:end+1])
        domains.iloc[i, 3] = end-start


def get_boundaries(matrix: np.matrix, tads: pd.DataFrame, chr_sizes: pd.DataFrame, chr: int, resol: int, window=0):
    chr_size = int(chr_sizes[chr_sizes.loc[:, 0] == f"chr{chr}"][1])
    end = chr_size
    schema = {"start": "int64", "end": "int64",
              "cf": "float64", "count": "int64"}
    boundaries = pd.DataFrame(columns=schema.keys()).astype(schema)
    tads_count = len(tads)
    i = 0
    s = 0
    e = 0
    for idx in range(0, tads_count):
        if idx == 0 and tads.iloc[idx, 0] > 0:
            s = 0 if tads.iloc[idx, 0] - \
                window < 0 else tads.iloc[idx, 0]-window
            e = tads.iloc[idx, 1]+window
            row = {"start": s, "end": e}
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            s = tads.iloc[idx, 1]-window
            e = tads.iloc[idx+1, 0] + window
            i = i+1
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1
        elif idx == tads_count-1 and tads.iloc[idx, 1] < end:
            s = tads.iloc[idx, 1]
            e = end
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1
        elif idx+1 < tads_count:
            s = tads.iloc[idx, 1]-window
            e = tads.iloc[idx+1, 0] + window
            row = {"start": s, "end": e}
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1

    get_cf(matrix=matrix, domains=boundaries, resol=resol)
    return boundaries

def tad_adj_r_square(matrix: np.matrix, tads: pd.DataFrame, boundaies: pd.DataFrame, resol: int, genomic_distance: int):
    num_bins = int(genomic_distance/resol)
    n = num_bins
    p = len(tads.loc[(tads["end"] - tads["start"] >= genomic_distance)])
    y_bar = np.mean(np.trace(matrix[0:num_bins+1, 0:num_bins+1]))
    denom = 0
    nume = 0
    for i in range(0, num_bins, 1):
        n = i+1
        y_i = matrix[i][i]
        y_hat_i = 0
        tads_frame = tads.loc[(tads["start"] >= 0) & (tads["end"] <= i*resol)]
        boundary_frame = boundaies.loc[(boundaies["start"] >= 0) & (boundaies["end"] <= i*resol)]
        if len(tads_frame) > 0:
            y_hat_i = tads_frame["cf"].sum()/tads_frame["count"].sum()
        elif len(boundary_frame) > 0:
            y_hat_i = boundary_frame["cf"].sum()/boundary_frame["count"].sum()
        denom += np.square(y_i - y_hat_i)
        nume += np.square(y_i - y_bar)

    denom = 0 if n-p-1 == 0 else (1/(n-p-1))*denom
    nume = 0 if n-1 == 0 else (1/(n-1))*nume

    return 0 if nume == 0 else 1 - (denom/nume)


def main():
    schema = {'bin': 'int8', 'score': 'float64'}
    r_square = pd.DataFrame(columns=schema.keys()).astype(schema)
    for organism, chr, chr_size_file, fn_prefix in zip(ORGANISMS, CHROMOSOMES, CHR_SIZE_FILES, FILENAME_PREFIXES):
        chr_sizes = pd.read_csv(
            f"{BASE_PATH}/{chr_size_file}", delimiter='\t', header=None)
        print(f"Organism: {organism}")
        for resol in RESOLUTIONS:
            matrix_file = f"{BASE_PATH}/matrix/{fn_prefix}_{resol}_chr{chr}.txt"
            matrix = np.loadtxt(matrix_file)
            res = "10K" if resol == 10000 else "5K"
            fig, ax = plt.subplots(figsize=(12, 6))
            for tad_filename, algo, color in zip(TAD_FILENAMES, ALGORITHMS, COLORS):
                print(f"{tad_filename}")
                tad_file = f"{BASE_PATH}/resutls/comparison/{organism.lower()}/{res}/{tad_filename}"
                tads = pd.read_csv(tad_file, delimiter=",", header=None)
                tads = tads.iloc[:, [0, 1]]
                tads.columns = ["start", "end"]
                tads["cf"] = 0
                tads["count"] = 0
                tads.sort_values(by=["start", "end"])
                get_cf(matrix=matrix, domains=tads, resol=resol)
                boundaries = get_boundaries(matrix=matrix, tads=tads, chr_sizes=chr_sizes, chr=chr, resol=resol)
                gd=int(1500000/resol)
                for i in range(0, gd+1, 1):
                    rsq = tad_adj_r_square(matrix=matrix, tads=tads, boundaies=boundaries, resol=resol, genomic_distance=i*resol)
                    new_row = {'bin': i, 'score': rsq}
                    r_square.loc[len(r_square)] = new_row

                ax.plot(r_square["bin"], r_square["score"], label=f"{algo}", color=color, linestyle='-')
                r_square.to_csv(f"{BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_tad_adj.txt", sep="\t")
            ax.set_xlabel("bin")
            ax.set_ylabel("$R^2_{TAD}$")
            ax.set_title(f"{organism} {chr} at {res}")
            ax.legend(fontsize=8, loc='upper right', frameon=True)
            print(f"Saving figure {BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_tad_adj.png")
            plt.savefig(f"{BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_tad_adj.png", dpi=300, bbox_inches="tight")
            plt.close()


if __name__ == "__main__":
    draw_boxplot()

import seaborn as sns
def draw_boxplot():
    df = pd.DataFrame(f"/home/mohit/Documents/project/EmbedTAD/data/resutls/comparison/TadadjRsqr.csv")
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Algorithm", y="TADadjRsquare", hue="Resolution", fill=False, gap=.1)
    plt.title("GM12878 10Kb")
    plt.xlabel(f"Algorithm")
    plt.ylabel(f"TADadjR$^2$")
