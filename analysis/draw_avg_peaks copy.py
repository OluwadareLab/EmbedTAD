import os
import pandas as pd
import math
import matplotlib.pyplot as plt


def get_average_peaks(tads: pd.DataFrame, ref_file: pd.DataFrame, chr_sizes: pd.DataFrame, chr: str, resol: int, window: int = 0):
    # Calculate chromosome size and pixel boundaries
    chr_size = int(chr_sizes.loc[chr_sizes.iloc[:, 0] == chr, 1].values[0])
    end_pixel = math.ceil(chr_size / resol) * resol

    # Extract reference values for the chromosome
    chr_ref_file = ref_file

    # Initialize the average_counts DataFrame
    lim = int(500 / (resol / 1000))
    idx_range = range(-lim, lim + 1)
    pixel_range = [(i * (resol / 1000)) for i in idx_range]
    average_counts = pd.DataFrame({
        "idx": idx_range,
        "pixel": pixel_range,
        "count": 0
    })

    # Process each TAD boundary pair
    boundaries_count = 0
    for i in range(len(tads) - 1):
        row_1, row_2 = tads.iloc[i, 1], tads.iloc[i + 1, 0]
        if row_1 == row_2:
            row_2 += resol
        get_peaks(row_1, row_2, 0, end_pixel, resol, lim,
                  chr_ref_file, average_counts, window)
        boundaries_count += 1

    # Normalize counts
    average_counts["count"] /= boundaries_count
    return average_counts


def get_peaks(start, end, start_pixel, end_pixel, resol, lim, chr_ref_file, average_counts, window):
    window = window if window > 0 else int(resol / 1000)
    boundaries = []

    n_idx, p_idx = -1, 1
    for offset in range(lim + 1):
        start_left = max(start - offset * resol, start_pixel)
        end_right = min(end + offset * resol, end_pixel)

        if start_left >= start_pixel:
            boundaries.append(
                {"idx": n_idx, "start": start_left, "end": start})
            n_idx -= 1
        if end_right <= end_pixel:
            boundaries.append({"idx": p_idx, "start": end, "end": end_right})
            p_idx += 1

    boundaries_df = pd.DataFrame(boundaries)
    for _, row in boundaries_df.iterrows():
        idx = row["idx"]
        lower_bound, upper_bound = row["start"] - window, row["end"] + window
        count = chr_ref_file[(chr_ref_file["start"] >= lower_bound) & (
            chr_ref_file["end"] <= upper_bound)].shape[0]
        average_counts.loc[average_counts["idx"] == idx, "count"] += count


def main():
    base_path = "/home/mohit/Documents/project/EmbedTAD/data"
    organisms = ["GM12878", "CH12LX"]
    chromosomes = [19, 18]
    resolutions = [5000, 10000]

    chr_size_files = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
    tad_filenames = ["EmbedTAD.bed", "Caspian.bed"]
    # tad_filenames = ["EmbedTAD.bed", "ClusterTAD.bed",
    #                  "HiCseg.bed", "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
    ref_filenames = [
        ["wgEncodeBroadHistoneGm12878CtcfStdPk.txt", "wgEncodeBroadHistoneGm12878H3k27acStdPk.txt",
         "wgEncodeBroadHistoneGm12878H3k27me3StdPkV2.txt", "wgEncodeBroadHistoneGm12878H3k4me1StdPk.txt",
         "wgEncodeBroadHistoneGm12878H3k4me3StdPk.txt", "wgEncodeBroadHistoneGm12878H3k9me3StdPk.txt",
         "wgEncodeOpenChromChipGm12878Pol2Pk.txt"],
        ["wgEncodeLicrHistoneCh12H3k27acFImmortalC57bl6StdPk.txt", "wgEncodeLicrHistoneCh12H3k36me3FImmortalC57bl6StdPk.txt",
         "wgEncodePsuHistoneCh12H3k27me3FImmortal2a4bInputPk.txt", "wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt",
         "wgEncodeSydhHistCh12H3k4me3IggyalePk.txt", "wgEncodeSydhTfbsCh12Pol2IggmusPk.txt"]
    ]
    labels = [
        ["CTCF", "H3k27ac", "H3k27me3", "H3k4me1", "H3k4me3", "H3k9me3", "Pol2"],
        ["H3k27ac", "H3k36me3", "H3k27me3", "Ctcf", "H3k4me3", "Pol2"]
    ]

    # Iterate over organisms, chromosomes, and chromosome size files
    for organism, chr_num, chr_size_file, ref_fns, og_labels in zip(organisms, chromosomes, chr_size_files, ref_filenames, labels):
        # Load chromosome size file once per organism
        chr_sizes = pd.read_csv(os.path.join(
            base_path, chr_size_file), delimiter='\t', header=None)
        chr_name = f"chr{chr_num}"

        # Print organism information
        print(f"Organism: {organism}")

        for resol in resolutions:
            print(f"Resolution: {resol}")
            plt.rcParams.update({'font.size': 22})
            colors = ['blue', 'green', 'red',
                      'purple', 'orange', 'cyan', 'magenta']
            res_str = "10K" if resol == 10000 else "5K"
            ref_folder = organism.lower()

            # Load and plot each reference file
            for ref_fn, label, color in zip(ref_fns, og_labels, colors):
                ref_file_path = os.path.join(
                    base_path, "chip_pk", ref_folder, ref_fn)
                print(f"{label}: {ref_fn}")

                # Load reference file once per label
                ref_file = pd.read_csv(
                    ref_file_path, delimiter="\t", header=None)
                ref_file = ref_file.loc[ref_file.iloc[:, 1]
                                        == chr_name, [2, 3]]
                ref_file.columns = ["start", "end"]

                # Process each TAD file once per resolution
                for tad_filename in tad_filenames:
                    tad_file_path = os.path.join(
                        base_path, "resutls", "comparison", ref_folder, res_str, tad_filename)
                    print(f"Processing TAD file: {tad_filename}")

                    # Load TAD file
                    tads = pd.read_csv(
                        tad_file_path, delimiter=",", header=None).iloc[:, [0, 1]]
                    tads.columns = ["start", "end"]

                    # Calculate average peaks
                    tad_peaks = get_average_peaks(
                        tads=tads, ref_file=ref_file, chr_sizes=chr_sizes, chr=chr_name, resol=resol
                    )

                    # Create a new plot for each TAD file and reference combination
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(tad_peaks["pixel"], tad_peaks["count"],
                            label=label, color=color)
                    ax.set_xlabel("Distance from TAD boundary (Kb)")
                    ax.set_ylabel(
                        f"Average {label} peaks per bin ({res_str}b)")
                    ax.set_title(
                        f"Average {label} peaks ({organism} {chr_name})")
                    ax.legend()

                    # Save the figure for the current TAD file and reference file
                    output_path = os.path.join(
                        base_path, "resutls", "comparison", f"{organism}_{res_str}_{chr_name}_{tad_filename}_{label}_average_peaks.png")
                    print(f"Saving figure: {output_path}")
                    fig.savefig(output_path, dpi=200, bbox_inches="tight")
                    plt.close(fig)


if __name__ == "__main__":
    main()
