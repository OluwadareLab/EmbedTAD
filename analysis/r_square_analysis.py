import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"
# ORGANISMS = ["GM12878", "CH12LX"]
ORGANISMS = ["GM12878"]
# CHROMOSOMES = [19, 18]
CHROMOSOMES = [19]
# RESOLUTIONS = [5000, 10000]
RESOLUTIONS = [10000]
# CHR_SIZE_FILES = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
CHR_SIZE_FILES = ["hg19.chrom.sizes"]
# TAD_FILENAMES = ["EmbedTAD.bed", "ClusterTAD.bed", "HiCseg.bed",
#                  "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
TAD_FILENAMES = ["EmbedTAD.bed"]
# ALGORITHMS = ["EmbedTAD", "ClusterTAD", "HiCseg",
#               "Spectral", "TopDom", "Armatus", "IC-Finder", "Caspian"]
ALGORITHMS = ["EmbedTAD"]
# COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#           '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
COLORS = ['#1f77b4']
# FILENAME_PREFIXES = ["gm12878_combined", "ch12lx"]
FILENAME_PREFIXES = ["gm12878_combined"]


def get_boundaries(matrix: np.matrix, tads: pd.DataFrame, chr_sizes: pd.DataFrame, chr: int, resol: int, window=0):
    chr_size = int(chr_sizes[chr_sizes.loc[:, 0] == f"chr{chr}"][1])
    end = chr_size
    schema = {"start": "int64", "end": "int64",
              "tcf": "float64", "count": "int64"}
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

    get_tcf(matrix=matrix, domains=boundaries, resol=resol)
    return boundaries


def get_tcf(matrix: np.matrix, domains: pd.DataFrame, resol):
    count = len(domains)
    for i in range(0, count, 1):
        start = int(domains.iloc[i, 0]/resol)
        end = int(domains.iloc[i, 1]/resol)
        domains.iloc[i, 2] = np.trace(matrix[start:end+1, start:end+1])
        domains.iloc[i, 3] = end-start
        # if i > 0:
            # domains.iloc[i, 2] = domains.iloc[i, 2] + domains.iloc[i-1, 2]
            # domains.iloc[i, 3] = domains.iloc[i, 3] + domains.iloc[i-1, 3]
            # domains.iloc[i, 2] = domains.iloc[i, 2]
            # domains.iloc[i, 3] = domains.iloc[i, 3]


def tad_adj_r_square(matrix: np.matrix, tads: pd.DataFrame, boundaies: pd.DataFrame, resol: int):
    num_bins = matrix.shape[0]
    schema = {'bin': 'int8', 'score': 'float64'}
    r_square = pd.DataFrame(columns=schema.keys()).astype(schema)
    yi_list = []
    yhati_list = []
    for i in range(0, num_bins, 1):
        y_i = matrix[i][i]
        yi_list.append(y_i)
        n = i+1
        tads_frame = tads.loc[(tads["start"] >= 0) & (tads["end"] <= n*resol)]
        p = len(tads_frame)
        y_hat_i = 0
        boundary_frame = boundaies.loc[(boundaies["start"] >= 0) & (
            boundaies["end"] <= n*resol)]
        not_p = len(boundary_frame)
        if p > 0:
            y_hat_i = tads_frame.iloc[len(
                tads_frame)-1, 2]/tads_frame.iloc[len(tads_frame)-1, 3]
        elif not_p > 0:
            y_hat_i = boundary_frame.iloc[len(
                boundary_frame)-1, 2]/boundary_frame.iloc[len(boundary_frame)-1, 3]

        yhati_list.append(y_hat_i)
        y_bar_i = np.mean(np.trace(matrix[0:i+1, 0:i+1]))

        r_sqr = 0
        if n-p-1 != 0 or n-1 != 0:
            deno = (1/(n-p-1))*np.sum([np.square(a_i - b_i)
                                       for a_i, b_i in zip(yi_list, yhati_list)])
            nume = (1/(n-1))*np.sum([np.square(a_i - y_bar_i)
                                     for a_i in yi_list])
            r_sqr = 0 if nume == 0 else 1 - (deno/nume)
        r_square = pd.concat([r_square, pd.DataFrame({"bin":i, "score":r_sqr}, index=[i])],  ignore_index=True)

    return r_square


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
                tads["tcf"] = 0
                tads["count"] = 0
                tads.sort_values(by=["start", "end"])
                get_tcf(matrix=matrix, domains=tads, resol=resol)
                boundaries = get_boundaries(
                    matrix=matrix, tads=tads, chr_sizes=chr_sizes, chr=chr, resol=resol)
                r_square = tad_adj_r_square(
                    matrix=matrix, tads=tads, boundaies=boundaries, resol=resol)
                ax.plot(r_square["bin"], r_square["score"],
                        label=f"{algo}", color=color, linestyle='-')
                r_square.to_csv(f"{BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_tad_adj.txt", sep="\t")
            ax.set_xlabel("bin")
            ax.set_ylabel("$R^2_{TAD}$")
            ax.set_title(f"{organism} {chr} at {res}")
            ax.legend(fontsize=8, loc='upper right', frameon=True)
            print(
                f"Saving figure {BASE_PATH}/resutls/comparison/{organism}_{res}_chr{chr}_tad_adj.png")
            plt.savefig(f"{BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_tad_adj.png",
                        dpi=300, bbox_inches="tight")
            plt.close()


if __name__ == "__main__":
    main()
