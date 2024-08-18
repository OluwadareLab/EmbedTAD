import pandas as pd
import math
import matplotlib.pyplot as plt


def get_average_peaks(tads: pd.DataFrame, ref_file: pd.DataFrame, chr_sizes: pd.DataFrame, chr: str, resol: int, window: int = 0):
    chr_size = int(chr_sizes[chr_sizes.iloc[:, 0] == chr][1])
    start_pixel = 0
    end_pixel = math.ceil(chr_size/resol)*resol

    # TAD region reformating
    # first_row = tads.iloc[0]
    # if first_row[0]>start_pixel:
    #     top = pd.Series([start_pixel, start_pixel])
    #     tads = pd.concat([top.to_frame().T, tads]).reset_index(drop=True)
    # last_row = tads.iloc[-1]
    # if last_row[1]<end_pixel:
    #     bottom = pd.Series([end_pixel, end_pixel])
    #     tads = pd.concat([bottom.to_frame().T, tads]).reset_index(drop=True)

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
        row_1 = tads.iloc[i]
        row_2 = tads.iloc[i+1]
        get_peaks(row_1[1], row_2[0], start_pixel, end_pixel,
                  resol, lim, chr_ref_file, average_counts, window)
        boundaries = boundaries + 1
        # if row_1[1] != row_2[0]:
        #     get_peaks(row_2[0], start_pixel, end_pixel,
        #               resol, lim, chr_ref_file, average_counts, window)
        #     boundaries = boundaries + 1

    average_counts["count"] = average_counts["count"]/boundaries
    return average_counts


def get_peaks(start, end, start_pixel, end_pixel, resol, lim, chr_ref_file, average_counts, window):
    boundaries = pd.DataFrame()
    boundaries["idx"] = ""
    boundaries["start"] = ""
    boundaries["end"] = ""
    # start = int(middle-(resol/2))
    # end = int(middle+(resol/2))
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
    for j in range(len(boundaries)):
        window = int(resol/1000) if window == 0 else window
        row = boundaries.iloc[j]
        idx = row["idx"]
        lower_bound = row["start"] - window
        upper_bound = row["end"] + window
        count = len(chr_ref_file[(chr_ref_file["start"] >= lower_bound) & (
            chr_ref_file["end"] <= upper_bound)])
        average_counts.loc[average_counts['idx'] == idx, "count"] += count


def main():
    # tad_file = "/home/mohit/Documents/project/EmbedTAD/data/resutls/cpu_GM12878_insitu_primary_30_10000_chr21_embed_tad.tsv"
    # tads = pd.read_csv(tad_file, delimiter="\t", header=None)
    # tads = tads.iloc[:, [1, 3]]
    # tads.columns = ["start", "end"]
    # ref_file = "/home/mohit/Documents/project/EmbedTAD/data/wgEncodeBroadChipSeqPeaksGm12878Ctcf.txt"
    # ctcf_refs = pd.read_csv(ref_file, delimiter="\t", header=None)
    # chr_size_file = "/home/mohit/Documents/project/project_drew/hg19.chrom.sizes"
    # chr_sizes = pd.read_csv(chr_size_file, delimiter='\t', header=None)
    # avg_peaks = get_average_peaks(tads=tads, ref_file=ctcf_refs,
    #                               chr_sizes=chr_sizes, chr="chr21", resol=10000, window=0)

    tad_file = "/home/mohit/Documents/project/project_drew/data/chr_19.bed"
    tads = pd.read_csv(tad_file, delimiter="\t", header=None)
    tads = tads.iloc[:, [0, 1]]
    tads.columns = ["start", "end"]
    # ref_file = "/home/mohit/Documents/project/project_drew/data/wgEncodeAwgTfbsBroadH1hescCtcfUniPk.txt"
    ref_file = "/home/mohit/Documents/project/project_drew/data/wgEncodeAwgTfbsHaibH1hescPol2V0416102UniPk.txt"
    # ref_file = "/home/mohit/Documents/project/project_drew/data/wgEncodeBroadHistoneH1hescH3k27acStdPk.txt"
    # ref_file = "/home/mohit/Documents/project/project_drew/data/wgEncodeBroadHistoneH1hescH3k4me1StdPk.txt"
    # ref_file = "/home/mohit/Documents/project/project_drew/data/wgEncodeBroadHistoneH1hescH3k4me3StdPk.txt"
    ctcf_refs = pd.read_csv(ref_file, delimiter="\t", header=None)
    chr_size_file = "/home/mohit/Documents/project/project_drew/data/hg19.chrom.sizes"
    chr_sizes = pd.read_csv(chr_size_file, delimiter='\t', header=None)
    avg_peaks = get_average_peaks(tads=tads, ref_file=ctcf_refs,
                                  chr_sizes=chr_sizes, chr="chr19", resol=40000)

    plt.plot(avg_peaks["pixel"], avg_peaks["count"])
    plt.xlabel("Distance from TAD boundary")
    plt.ylabel("Average RNA polymerase II peaks per bin (40Kb)")
    plt.title("Average RNA polymerase II Peaks (H1 hESC chr19)")
    plt.savefig("/home/mohit/Documents/project/project_drew/results/h1_hesc_40000_chr19_average_polii_peaks.png",
                dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    main()
