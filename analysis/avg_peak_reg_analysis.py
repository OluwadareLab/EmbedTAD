
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.interpolate import make_interp_spline


TAD_PATH = "/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/comparison"
TAD_FILENAMES = ["topdom.bed",
                 "hicseg.bed",
                 "spectral.bed",
                 "clustertad.bed",
                 "armatus.bed",
                 "ic_finder.bed",
                 "caspian.bed",
                 "embedtad.bed",]
ALGORITHMS = ["TopDom", "HiCSeg", "Spectral", "ClusterTAD",
              "Armatus", "IC-Finder", "Caspian", "EmbedTAD"]
# TAD_FILENAMES = ["topdom.bed", "embedtad.bed"]
# ALGORITHMS = ["TopDom", "EmbedTAD"]

CHIP_SEQ_SIG_PATH = "/home/hc0783.unt.ad.unt.edu/workspace/data/chip_seq_signals"
CHIP_SEQ_SIG_FILENAMES = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt"]]
CHIP_SEQ_NAMES = ["CTCF"]
RESOLUTIONS = [10000]
ORGANISMS = ["GM12878"]
CHROMOSOMES = [19]

TAD_COL_NAMES = ["start", "end"]
TAD_DTYPE_MAP = {
    "start": int,
    "end": int
}

WINDOWS = [40000, 20000]
LIMITS = [25, 25]
GEN_POINTS = [300, 300]


def get_css(css_file: np) -> pd:
    filtered_css = css_file[css_file[:, 1] == f"{chr_}"]
    sorted_css = filtered_css[filtered_css[:, 2].astype(float).argsort()]
    reduced_css = sorted_css[:, [2, 3, 7]]
    return pd.DataFrame({
        "start": reduced_css[:, 0].astype(int),
        "end": reduced_css[:, 1].astype(int),
        "signal_value": reduced_css[:, 2].astype(float)
    })


def plot_signal_df(signal_df: pd.DataFrame, org: str, res: int, chr: int, chip_name: str, window: int, normalize: str = None, smooth: bool = True, shading: bool = True, log: bool = False) -> None:
    df = signal_df.copy()

    if normalize == "minmax":
        df = (df - df.min()) / (df.max() - df.min())
    elif normalize == "zscore":
        df = (df - df.mean()) / df.std()

    positions = df.index.values
    x_new = np.linspace(positions.min(), positions.max(), gen_point)

    nature_colors = [
        "#000000", "#e69f00", "#56b3e9", "#009e74", "#f0e442", "#d55e00", "#cc79a7", "#0072b2",
    ]
    linestyles = ["--", "-.", ":", "-", "--", "-.", ":", "-",]

    plt.figure(figsize=(16, 10))

    for i, col in enumerate(df.columns):
        y = df[col].values
        color = nature_colors[i % len(nature_colors)]
        linestyle = linestyles[i % len(linestyles)]

        if smooth and len(positions) > 3:
            spline = make_interp_spline(positions, y, k=3)
            y_smooth = spline(x_new)
            plt.plot(
                x_new, y_smooth,
                label=col,
                linewidth=2.2,
                color=color,
                linestyle=linestyle
            )
            if shading:
                plt.fill_between(
                    x_new, y_smooth * 0.9, y_smooth * 1.1,
                    alpha=0.15, color=color
                )
        else:
            plt.plot(
                positions, y,
                label=col,
                linewidth=2.2,
                color=color,
                linestyle=linestyle
            )
            if shading:
                plt.fill_between(
                    positions, y * 0.9, y * 1.1,
                    alpha=0.15, color=color
                )
    # plt.axvline(x=0, color="black", linestyle="--", linewidth=1)

    if log:
        plt.yscale("log")
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.ticklabel_format(style="plain")

    # plt.xlabel("Distance from TAD boundary (kb)", fontsize=18)
    plt.ylabel("Normalized Signal", fontsize=18)
    plt.title(f"{chip_name}", fontsize=22, weight="bold")

    plt.legend(frameon=False, fontsize=14, ncol=2)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(
        f"avg_{org.lower()}_{chip_name.lower()}_{res}_chr{chr}_{window}_uni.png",
        dpi=600, bbox_inches="tight"
    )
    plt.close()


def cal_signals(css, start, window, limit, signal_df):
    for i in range(0, limit, 1):
        end = min(max_chr_bp, start+window)
        signals = css[(css["start"] >= start)
                      & (css["end"] <= end)]
        total_signal = signals["signal_value"].sum()
        signal_df.loc[i, algo] += total_signal
        start += window


for window in WINDOWS:
    for org, chr, chip_filenames in zip(ORGANISMS, CHROMOSOMES, CHIP_SEQ_SIG_FILENAMES):
        org_ = org.lower()
        chr_ = f"chr{chr}"
        max_chr_bp = 59128983
        for chip_name, chip_seq_sig_filename in zip(CHIP_SEQ_NAMES, chip_filenames):
            css_file = np.loadtxt(
                f"{CHIP_SEQ_SIG_PATH}/{org_}/{chip_seq_sig_filename}", delimiter="\t", dtype=str)
            css = get_css(css_file=css_file)
            total_sv = css["signal_value"].sum()
            for res, limit, gen_point in zip(RESOLUTIONS, LIMITS, GEN_POINTS):
                print(
                    f"ChIP-seq: {chip_name}, Organism: {org}, chromosome: {chr}, Resolution: {res}")
                interval = res//1000
                index_vals = np.arange(0, limit+1, 1)
                signal_df = pd.DataFrame(
                    0.00001, index=index_vals, columns=ALGORITHMS)
                for algo, filename in zip(ALGORITHMS, TAD_FILENAMES):
                    bldf_idx = 0
                    print(f"Algorithm: {algo}")
                    tad_file = pd.read_csv(
                        f"{TAD_PATH}/{org_}/{org_}_{res}_{chr_}_{filename}",
                        sep=",",
                        header=None,
                        names=TAD_COL_NAMES,
                        dtype=TAD_DTYPE_MAP
                    )
                    if algo == "Armatus":
                        tad_file["end"] += 1
                    tad_count = len(tad_file)

                    for i in range(tad_count-1):
                        b_start = tad_file.iloc[i]["end"].astype(int)
                        b_end = tad_file.iloc[i+1]["start"].astype(int)
                        b_start = b_start + (b_end-b_start)//2
                        cal_signals(css=css, start=b_start,
                                    window=window, limit=limit, signal_df=signal_df)

                        # b_start = tad_file.iloc[i]["end"].astype(int)
                        # cal_signals(css=css, start=b_start,
                        #             window=window, limit=limit, signal_df=signal_df)

                    # signal_df[algo] /= (boundary_count+1)
                    # signal_df[algo] /= total_sv
                    # signal_df[algo] = np.log10(signal_df[algo])
                plot_signal_df(signal_df=signal_df, org=org, res=res, chr=chr, chip_name=chip_name, window=window,
                               normalize="zscore", smooth=False, shading=False, log=False)
