
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
# TAD_FILENAMES = ["embedtad.bed"]
# ALGORITHMS = ["EmbedTAD"]

CHIP_SEQ_SIG_PATH = "/home/hc0783.unt.ad.unt.edu/workspace/data/chip_seq_signals"
CHIP_SEQ_SIG_FILENAMES = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt"],
                          ["wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt"]]
CHIP_SEQ_NAMES = ["CTCF"]
RESOLUTIONS = [5000, 10000]
ORGANISMS = ["GM12878", "CH12LX"]
CHROMOSOMES = [19, 18]

TAD_COL_NAMES = ["start", "end"]
TAD_DTYPE_MAP = {
    "start": int,
    "end": int
}

EXPAND_FACTOR = 1
GEN_POINTS = [300, 300]
TB_REGIONS = [150, 150]


def get_css(css_file: np) -> pd:
    filtered_css = css_file[css_file[:, 1] == f"{chr_}"]
    sorted_css = filtered_css[filtered_css[:, 2].astype(float).argsort()]
    reduced_css = sorted_css[:, [2, 3, 7]]
    return pd.DataFrame({
        "start": reduced_css[:, 0].astype(int),
        "end": reduced_css[:, 1].astype(int),
        "signal_value": reduced_css[:, 2].astype(float)
    })


def cal_us_ds_signals(css, b_start, b_end, res, index_vals, signal_df, algo):
    signals = css[(css["start"] >= b_start) & (css["end"] <= b_end)]
    total_signal = signals["signal_value"].sum()
    signal_df.loc[0, algo] += total_signal
    # downstream
    # print(f"Downstream")
    ds_idx = 0
    ds_bp_lim = max(0, b_start-(res*(len(index_vals)//2)))
    for ds_bp in range(b_start, ds_bp_lim, -res):
        ds_start = max(0, ds_bp - res)
        ds_end = ds_bp
        signals = css[(css["start"] >= ds_start) & (css["end"] <= ds_end)]
        total_signal = signals["signal_value"].sum()
        ds_idx = ds_idx-res//1000
        signal_df.loc[ds_idx, algo] += total_signal
        # print(f"Idx: {ds_idx}, Strat: {ds_start}, End: {ds_end}")

    # upstream
    # print(f"Upstream")
    us_idx = 0
    us_bp_lim = min(max_chr_bp, b_end+(res*(len(index_vals)//2)))
    for us_bp in range(b_end, us_bp_lim, res):
        us_start = us_bp
        us_end = max(0, us_bp + res)
        signals = css[(css["start"] >= us_start) & (css["end"] <= us_end)]
        total_signal = signals["signal_value"].sum()
        us_idx = us_idx+res//1000
        signal_df.loc[us_idx, algo] += total_signal
        # print(f"Idx: {us_idx}, Strat: {us_start}, End: {us_end}")

# def plot_signal_df(signal_df, org, res, chr, chip_name, normalize=None, smooth=True, shading=True, log=False):
#     df = signal_df.copy()

#     if normalize == "minmax":
#         df = (df - df.min()) / (df.max() - df.min())
#     elif normalize == "zscore":
#         df = (df - df.mean()) / df.std()

#     positions = df.index.values
#     x_new = np.linspace(positions.min(), positions.max(), GEN_POINTS)

#     plt.figure(figsize=(16,10))
#     for col in df.columns:
#         y = df[col].values

#         # Smooth curve
#         if smooth and len(positions) > 3:
#             spline = make_interp_spline(positions, y, k=3)
#             y_smooth = spline(x_new)
#             plt.plot(x_new, y_smooth, label=col, linewidth=2)
#             if shading:
#                 plt.fill_between(x_new, y_smooth*0.9, y_smooth*1.1, alpha=0.2)
#         else:
#             plt.plot(positions, y, label=col, linewidth=2)
#             if shading:
#                 plt.fill_between(positions, y*0.9, y*1.1, alpha=0.2)

#     plt.axvline(x=0, color="black", linestyle="--", linewidth=1)

#     if log:
#         plt.yscale("log")
#         ax = plt.gca()
#         ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
#         ax.yaxis.set_minor_formatter(mticker.NullFormatter())
#         ax.ticklabel_format(style="plain")

#     plt.xlabel(f"Distance from TAD boundary (kb)", fontsize=16)
#     plt.ylabel(f"Normalized Signal", fontsize=16)
#     plt.title(f"{chip_name}", fontsize=20, weight="bold")
#     plt.legend(frameon=False)
#     plt.savefig(f"avg_{org.lower()}_{chip_name.lower()}_{res}_chr{chr}.png", dpi=300, bbox_inches="tight")
#     plt.close()


def plot_signal_df(signal_df: pd.DataFrame, org: str, res: int, chr: int, chip_name: str, normalize: str = None, smooth: bool = True, gen_point: int = 150, shading: bool = True, log: bool = False) -> None:
    # Copy original DF
    df = signal_df.copy()

    # Normalization
    if normalize == "minmax":
        df = (df - df.min()) / (df.max() - df.min())
    elif normalize == "zscore":
        df = (df - df.mean()) / df.std()

    positions = df.index.values
    x_new = np.linspace(positions.min(), positions.max(), gen_point)

    nature_colors = [
        "#000000", "#e69f00", "#56b3e9", "#009e74", "#f0e442", "#d55e00", "#cc79a7", "#0072b2",
    ]

    # Alternate solid and dashed lines for visibility
    linestyles = ["--", "-.", ":", "-", "--", "-.", ":", "-",]

    plt.figure(figsize=(16, 10))

    for i, col in enumerate(df.columns):
        y = df[col].values
        color = nature_colors[i % len(nature_colors)]
        linestyle = linestyles[i % len(linestyles)]

        # Smooth curve if requested
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

    # Add vertical reference line
    # plt.axvline(x=0, color="black", linestyle="--", linewidth=1)

    # Log scale option
    if log:
        plt.yscale("log")
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.ticklabel_format(style="plain")

    # Labels and title
    plt.xlabel("Distance from TAD boundary (kb)", fontsize=18)
    plt.ylabel("Normalized Signal", fontsize=18)
    plt.title(f"{chip_name}", fontsize=22, weight="bold")

    # Legend with two columns for readability
    plt.legend(frameon=False, fontsize=14, ncol=2)

    # Clean ticks
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Save high-res figure
    plt.savefig(
        f"avg_{org.lower()}_{chip_name.lower()}_{res}_chr{chr}_{EXPAND_FACTOR}.png",
        dpi=600, bbox_inches="tight"
    )
    plt.close()


for org, chr, chip_filenames in zip(ORGANISMS, CHROMOSOMES, CHIP_SEQ_SIG_FILENAMES):
    org_ = org.lower()
    chr_ = f"chr{chr}"
    max_chr_bp = 59128983
    for chip_name, chip_seq_sig_filename in zip(CHIP_SEQ_NAMES, chip_filenames):
        css_file = np.loadtxt(
            f"{CHIP_SEQ_SIG_PATH}/{org_}/{chip_seq_sig_filename}", delimiter="\t", dtype=str)
        css = get_css(css_file=css_file)
        total_sv = css["signal_value"].sum()
        for res, tb_region, gen_point in zip(RESOLUTIONS, TB_REGIONS, GEN_POINTS):
            print(
                f"ChIP-seq: {chip_name}, Organism: {org}, chromosome: {chr}, Resolution: {res}")
            expected_tb_region = res*EXPAND_FACTOR
            interval = res//1000
            index_vals = np.arange(-tb_region, tb_region+1, interval)
            signal_df = pd.DataFrame(
                0.00001, index=index_vals, columns=ALGORITHMS)
            boundary_len_df = pd.DataFrame(columns=ALGORITHMS)
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
                # at start
                # print(f"Start Position")
                b_start = 0
                b_end = tad_file.iloc[0]["start"].astype(int)
                boundary_len = b_end - b_start
                boundary_len_df.loc[bldf_idx, algo] = boundary_len
                bldf_idx += 1
                remaining_bl = 0
                if boundary_len < expected_tb_region:
                    remaining_bl = expected_tb_region - boundary_len
                    b_start = max(0, b_start - remaining_bl//2)
                    b_end = min(max_chr_bp, b_end + remaining_bl//2)
                # print(f"Boundary length: {boundary_len}, Remaining BL: {remaining_bl}, Strat: {b_start}, End: {b_end}")
                cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                                  index_vals=index_vals, signal_df=signal_df, algo=algo)

                # at middle
                # print(f"Middle Position")
                boundary_count = len(tad_file) - 1
                for i in range(boundary_count):
                    current_row = tad_file.iloc[i]
                    next_row = tad_file.iloc[i + 1]
                    b_start = current_row["end"].astype(int)
                    b_end = next_row["start"].astype(int)
                    boundary_len = b_end - b_start
                    boundary_len_df.loc[bldf_idx, algo] = boundary_len
                    bldf_idx += 1
                    remaining_bl = 0
                    if boundary_len < expected_tb_region:
                        remaining_bl = expected_tb_region - boundary_len
                        b_start = max(0, b_start - remaining_bl//2)
                        b_end = min(max_chr_bp, b_end + remaining_bl//2)
                    # print(f"Boundary length: {boundary_len}, Remaining BL: {remaining_bl}, Strat: {b_start}, End: {b_end}")
                    cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                                      index_vals=index_vals, signal_df=signal_df, algo=algo)

                # at end
                # print(f"End Position")
                b_start = tad_file.iloc[-1]["end"].astype(int)
                b_end = max_chr_bp
                boundary_len = b_end - b_start
                boundary_len_df.loc[bldf_idx, algo] = boundary_len
                bldf_idx += 1
                remaining_bl = 0
                if boundary_len < expected_tb_region:
                    remaining_bl = expected_tb_region - boundary_len
                    b_start = max(0, b_start - remaining_bl//2)
                    b_end = min(max_chr_bp, b_end + remaining_bl//2)
                # print(f"Boundary length: {boundary_len}, Remaining BL: {remaining_bl}, Strat: {b_start}, End: {b_end}")
                cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                                  index_vals=index_vals, signal_df=signal_df, algo=algo)
                # signal_df[algo] /= (boundary_count+1)
                # signal_df[algo] /= total_sv
                signal_df[algo] = np.log10(signal_df[algo])
            boundary_len_df.to_csv(
                f"avg_{org.lower()}_{chip_name.lower()}_{res}_chr{chr}.csv", index=False)
            plot_signal_df(signal_df=signal_df, org=org, res=res, chr=chr, chip_name=chip_name,
                           normalize="zscore", smooth=True, gen_point=gen_point, shading=False, log=False)
