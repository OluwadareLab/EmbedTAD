import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import make_interp_spline
import warnings
warnings.simplefilter(action='ignore')


BASE_PATH = "/home/mohit/Documents/project/embed_tad/data"
ORGANISMS = ["GM12878", "CH12.LX"]
CHROMOSOMES = [19, 18]
RESOLUTIONS = [5000]
CHR_SIZE_FILES = ["hg19.chrom.sizes", "mm10.chrom.sizes"]
TAD_FILE_PREFIX = ["gm12878", "ch12lx"]
TAD_FILE_SUFFIX = ["embedtad.bed", "clustertad.bed", "hicseg.bed",
                   "spectral.bed", "topdom.bed", "armatus.bed", "ic_finder.bed", "caspian.bed"]
SIGNAL_FILENAMES = [["gm12878_ctcf.bedgraph",
                     "gm12878_rad21.bedgraph",
                     "gm12878_smc3.bedgraph"],
                    ["ch12lx_ctcf.bedgraph",
                     "ch12lx_rad21.bedgraph",
                     "ch12lx_smc3.bedgraph"]]
LABELS = [["CTCF", "RAD21", "SMC3"], ["CTCF", "RAD21", "SMC3"]]
ALGORITHMS = ["EmbedTAD", "ClusterTAD", "HiCseg",
              "Spectral", "TopDom", "Armatus", "IC-Finder", "CASPIAN"]
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


def get_average_peaks(boundaries: pd.DataFrame, ref_file: pd.DataFrame, chr_sizes: pd.DataFrame, average_sv: pd.DataFrame, lim: int, chr: str, resol: int, window: int = 0):
    chr_size = int(
        chr_sizes.loc[chr_sizes.iloc[:, 0] == f"chr{chr}", 1].values[0])
    total_boundaries = len(boundaries)
    for idx in range(0, total_boundaries):
        s = boundaries.iloc[idx]["start"]
        e = boundaries.iloc[idx]["end"]
        pixels = np.arange(s - resol*lim, s, resol)
        pixels = np.append(pixels, [s, e])
        pixels = np.append(pixels, np.arange(e+resol, e+(lim+1)*resol, resol))
        for i in range(0, len(pixels)-1):
            bs = pixels[i]
            be = pixels[i+1]
            if bs >= 0 and be >= 0 and bs <= chr_size and be <= chr_size:
                score_frame = ref_file.loc[(ref_file["start"] >= bs) & (
                    ref_file["end"] <= be)]
                # score = score_frame["score"].sum()
                signalValue = score_frame["signalValue"].sum()
                # average_sv.loc[i, "score"] = average_sv.loc[i, "score"] + score
                average_sv.loc[i, "signalValue"] = average_sv.loc[i,
                                                                  "signalValue"] + signalValue
    # average_sv["score"] = average_sv["score"]/total_boundaries
    average_sv["signalValue"] = average_sv["signalValue"]/total_boundaries
    # average_sv["score"] = np.log10(average_sv["score"])
    average_sv["signalValue"] = np.log10(average_sv["signalValue"])
    # print(average_sv)


def get_boundary_score(start, end, ref_file):
    score = 0.0
    signalValue = 0.0
    peak_frame = ref_file.loc[(ref_file["start"] >= start)
                              & (ref_file["end"] <= end)]
    score = peak_frame["score"].sum()
    signalValue = peak_frame["signalValue"].sum()
    return score, signalValue


def get_boundaries(tad_file, chr_sizes, chr, window=50):
    tads = pd.read_csv(tad_file, delimiter=",", header=None)
    tads = tads.iloc[:, [0, 1]]
    tads.columns = ["start", "end"]
    tads.sort_values(by=["start", "end"])
    chr_size = int(chr_sizes[chr_sizes.loc[:, 0] == f"chr{chr}"][1])
    end = chr_size
    schema = {'start': 'int64', 'end': 'int64'}
    boundaries = pd.DataFrame(columns=schema.keys()).astype(schema)
    tads_count = len(tads)
    i = 0
    s = 0
    e = 0
    for idx in range(0, tads_count):
        if idx == 0 and tads.iloc[idx]["start"] > 0:
            s = 0 if tads.iloc[idx]["start"] - \
                window < 0 else tads.iloc[idx]["start"]-window
            e = tads.iloc[idx]["end"]+window
            row = {"start": s, "end": e}
            boundaries = pd.concat(
                [boundaries, pd.DataFrame(row, index=[i])],  ignore_index=True)
            s = tads.iloc[idx]["end"]-window
            e = tads.iloc[idx+1]["start"] + window
            i = i+1
            row = {"start": s, "end": e}
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1
        elif idx == tads_count-1 and tads.iloc[idx]["end"] < end:
            s = tads.iloc[idx]["end"]
            e = end
            row = {"start": s, "end": e}
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1
        elif idx+1 < tads_count:
            s = tads.iloc[idx]["end"]-window
            e = tads.iloc[idx+1]["start"] + window
            row = {"start": s, "end": e}
            boundaries = pd.concat([boundaries, pd.DataFrame(
                row, index=[i])],  ignore_index=True)
            i = i+1

    return boundaries


def is_nan_inf(arr):
    return np.any(np.isinf(arr) | np.isnan(arr))


def main():
    schema = {'idx': 'int8', 'signalValue': 'float64'}
    average_sv = pd.DataFrame(columns=schema.keys()).astype(schema)

    for organism, chr, chr_size_file, ref_fns, og_labels, prefix in zip(ORGANISMS, CHROMOSOMES, CHR_SIZE_FILES, SIGNAL_FILENAMES, LABELS, TAD_FILE_PREFIX):
        chr_sizes = pd.read_csv(
            f"{BASE_PATH}/raw/{chr_size_file}", delimiter='\t', header=None)
        print(f"Organism: {organism}")
        for resol in RESOLUTIONS:
            lim = 25 if resol == 10000 else 50
            # average_sv["idx"] = np.arange(-lim, (lim+1), 1)
            print(f"Resolution: {resol}")
            plt.rcParams.update({'font.size': 10})
            row = 1
            col = 3
            fig, axes = plt.subplots(row, col, figsize=(16, 4))
            for ax, ref_fn, label in zip(axes.flat, ref_fns, og_labels):
                print(f"{label}: {ref_fn}")
                ref_file = f"{BASE_PATH}/raw/chip_signals/{ref_fn}"
                ref_file = pd.read_csv(
                    ref_file, delimiter="\t", header=None, index_col=None)
                ref_file = ref_file.loc[ref_file.iloc[:, 0] == f"chr{chr}", [
                    1, 2, 3]].reset_index(drop=True)
                ref_file.columns = ["start", "end", "signalValue"]
                ref_file.sort_values(by=["start", "end"])
                res = "10K" if resol == 10000 else "5K"
                ymax = 0
                could_draw = False

                for suffix, algo, color in zip(TAD_FILE_SUFFIX, ALGORITHMS, COLORS):
                    print(f"{suffix}")
                    tad_file = f"{BASE_PATH}/results/tad_callers/{prefix}_{resol}_chr{chr}_{suffix}"
                    boundaries = get_boundaries(
                        tad_file, chr_sizes, chr, 50)

                    average_sv["idx"] = np.arange(-lim, (lim+1), 1)
                    # average_sv["score"] = 0.0
                    average_sv["signalValue"] = 0.0

                    get_average_peaks(
                        boundaries=boundaries, ref_file=ref_file, chr_sizes=chr_sizes, average_sv=average_sv, lim=lim, chr=chr, resol=resol
                    )
                    x = average_sv["idx"]
                    y = average_sv["signalValue"]
                    could_draw = could_draw or True if len(y) > 0 else False
                    if could_draw:
                        # y = (y - np.min(y)) / (np.max(y) - np.min(y))
                        if (is_nan_inf(y)):
                            print(f"Contains nan or inf values")
                            continue
                        x_smooth = np.linspace(
                            x.min(), x.max(), lim*10)
                        spl = make_interp_spline(x, y, k=3)  # Cubic spline
                        y_smooth = spl(x_smooth)
                        ymax = max(ymax, np.max(y))
                        ax.plot(x_smooth, y_smooth,
                                label=f"{algo}", color=color, linestyle='-')

                        # ax.plot(x, y, label=f"{algo}", color=color, linestyle='-')

                        # Positions on the x-axis
                        custom_ticks = [-25, -12, 0, 12,
                                        25] if resol == 10000 else [-50, -25, 0, 25, 50]
                        # Corresponding labels
                        custom_labels = ["-250Kb", "-120Kb",
                                         "0Kb", "120Kb", "250Kb"]

                        ax.set_xticks(custom_ticks)
                        ax.set_xticklabels(custom_labels)
                if could_draw:
                    ax.set_xlabel("Relative position")
                    # ax.set_ylabel("$log_{10}$(avg. signal value)")
                    ax.set_ylabel(f"Average signal")
                    # ax.set_ylim(-0.5, ymax+0.10)
                    ax.set_title(f"{label}")
                    # loc='best' places it optimally, frameon=False removes the box
                    ax.legend(loc='upper right', frameon=True, fontsize=8)
            # fig.suptitle(f"{organism} chr{chr} at {res}b", fontsize=24)
            output_file = f"/home/mohit/Documents/project/embed_tad/plots/{organism}_{res}_chr{chr}_average_peaks.png"
            print(f"Saving figure {output_file}")
            plt.savefig(output_file, dpi=600, bbox_inches="tight")
            plt.close()


if __name__ == "__main__":
    main()
