import pandas as pd
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def get_average_peaks(tads: pd.DataFrame, ref_file: pd.DataFrame, chr_sizes: pd.DataFrame, chr: str, resol: int, window: int = 0):
    chr_size = int(chr_sizes[chr_sizes.loc[:, 0] == chr][1])
    start_pixel = 0
    end_pixel = math.ceil(chr_size/resol)*resol

    # extract ref values
    chr_ref_file = ref_file.loc[ref_file.iloc[:, 1] == chr, [2, 3]]
    chr_ref_file.columns = ["start", "end"]

    # Create indexed count
    average_counts = pd.DataFrame()
    average_counts["idx"] = ""
    average_counts["pixel"] = ""
    average_counts["count"] = ""
    str_pxl = -500
    lim = int(500/(resol/1000))
    for i in range(-lim, lim+1, 1):
        average_counts.loc[len(average_counts.index)] = [i, str_pxl, 0]
        str_pxl = str_pxl+(resol/1000)

    # Generate bins for every new boundaries
    boundaries = 0
    for i in range(len(tads) - 1):
        row_1 = tads.iloc[i][1]
        row_2 = tads.iloc[i+1][0]
        if row_1 == row_2:
            row_2 = row_2 + resol
        get_peaks(row_1, row_2, start_pixel, end_pixel,
                  resol, lim, chr_ref_file, average_counts, window)
        boundaries = boundaries + 1

    average_counts["count"] = average_counts["count"]/boundaries
    return average_counts


def get_peaks(start, end, start_pixel, end_pixel, resol, lim, chr_ref_file, average_counts, window):
    boundaries = pd.DataFrame()
    boundaries["idx"] = ""
    boundaries["start"] = ""
    boundaries["end"] = ""
    boundaries.loc[len(boundaries.index)] = [
        0, start if start >= 0 else start_pixel, end if end <= end_pixel else end_pixel]
    flag = 0
    n_idx = -1
    p_idx = 1
    while n_idx >= -lim or p_idx <= lim:
        tmp = start
        start = start-resol
        if start >= start_pixel:
            boundaries.loc[len(boundaries.index)] = [n_idx, start, tmp]
            n_idx = n_idx-1
            flag = flag + 1
        tmp = end
        end = end+resol
        if end <= end_pixel:
            boundaries.loc[len(boundaries.index)] = [p_idx, tmp, end]
            p_idx = p_idx+1
            flag = flag + 1
        if flag > 0:
            flag = 0
        else:
            break

    window = int(resol/1000) if window == 0 else window
    for j in range(len(boundaries)):
        row = boundaries.loc[j]
        idx = row["idx"]
        lower_bound = row["start"] - window
        upper_bound = row["end"] + window
        count = len(chr_ref_file[(chr_ref_file["start"] >= lower_bound) & (
            chr_ref_file["end"] <= upper_bound)])
        average_counts.loc[average_counts['idx'] == idx, "count"] += count


def main():
    base_path = "/home/mohit/Documents/project/EmbedTAD/data"
    organisms = ["GM12878", "CH12LX"]
    chromosomes = [19, 18]
    resolutions = [10000]

    chr_size_files = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
    tad_filenames = ["EmbedTAD.bed", "ClusterTAD.bed", "HiCseg.bed", "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
    ref_filenames = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt",
                     "wgEncodeBroadHistoneGm12878H3k27acStdPk.txt",
                      "wgEncodeBroadHistoneGm12878H3k27me3StdPkV2.txt",
                      "wgEncodeBroadHistoneGm12878H3k4me1StdPk.txt",
                      "wgEncodeBroadHistoneGm12878H3k4me3StdPk.txt",
                      "wgEncodeBroadHistoneGm12878H3k9me3StdPk.txt",
                      "wgEncodeOpenChromChipGm12878Pol2Pk.txt"],
                     ["wgEncodeLicrHistoneCh12H3k27acFImmortalC57bl6StdPk.txt",
                      "wgEncodeLicrHistoneCh12H3k36me3FImmortalC57bl6StdPk.txt",
                      "wgEncodePsuHistoneCh12H3k27me3FImmortal2a4bInputPk.txt",
                      "wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt",
                      "wgEncodeSydhHistCh12H3k4me3IggyalePk.txt",
                      "wgEncodeSydhTfbsCh12Pol2IggmusPk.txt"]]
    labels = [["CTCF", "H3k27ac", "H3k27me3", "H3k4me1", "H3k4me3", "H3k9me3",
               "Pol2"], ["H3k27ac", "H3k36me3", "H3k27me3", "Ctcf", "H3k4me3", "Pol2"]]
    algos = ["EmbedTAD", "ClusterTAD", "HiCseg", "Spectral", "TopDom", "Armatus", "IC-Finder", "Caspian"]
    for organism, chr, chr_size_file, ref_fns, og_labels in zip(organisms, chromosomes, chr_size_files, ref_filenames, labels):
        chr_sizes = pd.read_csv(
            f"{base_path}/{chr_size_file}", delimiter='\t', header=None)
        print(f"Organism: {organism}")
        for resol in resolutions:
            print(f"Resolution: {resol}")
            plt.rcParams.update({'font.size': 22})
            # colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


            for ref_fn, label in zip(ref_fns, og_labels):
                print(f"{label}: {ref_fn}")
                ref_folder = organism.lower()
                ref_file = f"{base_path}/chip_pk/{ref_folder}/{ref_fn}"
                ref_file = pd.read_csv(ref_file, delimiter="\t", header=None)
                res = "10K" if resol == 10000 else "5K"

                fig, ax = plt.subplots(figsize=(10, 6))
                for tad_filename, algo, color in zip(tad_filenames, algos, colors):
                    print(f"{tad_filename}")
                    tad_file = f"{base_path}/resutls/comparison/{ref_folder}/{res}/{tad_filename}"
                    tads = pd.read_csv(tad_file, delimiter=",", header=None)
                    tads = tads.iloc[:, [0, 1]]
                    tads.columns = ["start", "end"]
                    tad_peaks = get_average_peaks(
                        tads=tads, ref_file=ref_file, chr_sizes=chr_sizes, chr=f"chr{chr}", resol=resol
                    )
                    ax.plot(tad_peaks["pixel"], tad_peaks["count"],
                            label=f"{algo}", color=color, linestyle='-')

                ax.set_xlabel("Distance from TAD boundary (Kb)")
                ax.set_ylabel(f"Average {label} peaks per bin ({res}b)")
                ax.set_title(f"Average {label} peaks ({organism} chr{chr})")
                ax.legend()
                print(
                    f"Saving figure {base_path}/resutls/comparison/{organism}_{res}_chr{chr}_average_{label}_peaks.png")
                plt.savefig(f"{base_path}/resutls/comparison/{organism}_{res}_chr{chr}_average_{label}_peaks.png",
                            dpi=200, bbox_inches="tight")
                plt.close()


if __name__ == "__main__":
    main()
