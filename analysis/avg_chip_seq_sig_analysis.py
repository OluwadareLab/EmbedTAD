
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.interpolate import make_interp_spline, interp1d

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

# TAD_FILENAMES = ["topdom.bed", "spectral.bed"]
# ALGORITHMS = ["TopDom", "Spectral"]


# TAD_FILENAMES = ["topdom.bed", "embedtad.bed"]
# ALGORITHMS = ["TopDom", "EmbedTAD"]

CHIP_SEQ_SIG_PATH = "/home/hc0783.unt.ad.unt.edu/workspace/data/chip_seq_signals"
CHIP_SEQ_SIG_FILENAMES = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt",
                           "wgEncodeAwgTfbsHaibGm12878Rad21V0416101UniPk.txt",
                           "wgEncodeAwgTfbsSydhGm12878Smc3ab9263IggmusUniPk.txt"],
                          ["wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt",
                           "wgEncodeSydhTfbsCh12Rad21IggrabPk.txt",
                           "wgEncodeSydhTfbsCh12Smc3ab9263IggrabPk.txt"]]
CHIP_SEQ_NAMES = ["CTCF", "RAD21", "SMC3"]
RESOLUTIONS = [5000, 10000]
ORGANISMS = ["GM12878", "CH12LX"]
CHROM_SIZES = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
CHROMOSOMES = [19, 18]

# CHIP_SEQ_SIG_FILENAMES = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt"],
#                           ["wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt"]]
# CHIP_SEQ_NAMES = ["CTCF"]
# RESOLUTIONS = [5000, 10000]
# ORGANISMS = ["GM12878"]
# CHROM_SIZES = ["hg19.chrom.sizes"]
# CHROMOSOMES = [19]

TAD_COL_NAMES = ["start", "end"]
TAD_DTYPE_MAP = {
    "start": int,
    "end": int
}

EXPAND_FACTOR = 2
GEN_POINTS = [201, 201]
TB_REGIONS = [250, 250]


def get_css(css_file: np) -> pd:
    filtered_css = css_file[css_file[:, 1] == f"{chr_}"]
    sorted_css = filtered_css[filtered_css[:, 2].astype(float).argsort()]
    reduced_css = sorted_css[:, [2, 3, 7]]
    return pd.DataFrame({
        "start": reduced_css[:, 0].astype(int),
        "end": reduced_css[:, 1].astype(int),
        "signal_value": reduced_css[:, 2].astype(float)
    })


def plot_signal_df(signal_df: pd.DataFrame, org: str, res: int, chr: int, chip_name: str, normalize: str = None, smooth: bool = True, gen_point: int = 150, shading: bool = True, log: bool = False) -> None:
    df = signal_df.copy()
    if normalize == "minmax":
        df = (df - df.min()) / (df.max() - df.min())
    elif normalize == "zscore":
        df = (df - df.mean()) / df.std()

    nature_colors = [
        "#000000", "#e69f00", "#56b3e9", "#009e74", "#f0e442", "#d55e00", "#cc79a7", "#0072b2",
    ]
    linestyles = ["--", "-.", ":", "-", "--", "-.", ":", "-",]

    plt.figure(figsize=(16, 10))
    positions = df.index.values
    new_index = np.arange(positions.min(), positions.max()+1)

    new_df = pd.DataFrame()
    new_df.index = new_index
    for i, col in enumerate(df.columns):
        color = nature_colors[i % len(nature_colors)]
        linestyle = linestyles[i % len(linestyles)]
        interpolate = interp1d(df.index, df[col], kind='cubic')
        new_df[col] = interpolate(new_index)
        plt.plot(
            new_df.index, new_df[col],
            label=col,
            linewidth=2.2,
            color=color,
            linestyle=linestyle
        )

    # positions = df.index.values
    # x_smooth = np.linspace(positions.min(), positions.max(), 351)
    # for i, col in enumerate(df.columns):
    #     y = df[col].values
    #     color = nature_colors[i % len(nature_colors)]
    #     linestyle = linestyles[i % len(linestyles)]

    #     if smooth and len(positions) > 3:
    #         spline = make_interp_spline(positions, y, k=3)
    #         y_smooth = spline(x_smooth)
    #         plt.plot(
    #             x_smooth, y_smooth,
    #             label=col,
    #             linewidth=2.2,
    #             color=color,
    #             linestyle=linestyle
    #         )
    #         if shading:
    #             plt.fill_between(
    #                 x_smooth, y_smooth * 0.9, y_smooth * 1.1,
    #                 alpha=0.15, color=color
    #             )
    #     else:
    #         plt.plot(
    #             positions, y,
    #             label=col,
    #             linewidth=2.2,
    #             color=color,
    #             linestyle=linestyle
    #         )
    #         if shading:
    #             plt.fill_between(
    #                 positions, y * 0.9, y * 1.1,
    #                 alpha=0.15, color=color
    #             )

    if log:
        plt.yscale("log")
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.ticklabel_format(style="plain")

    plt.xlabel("Distance from TAD boundary (Kb)", fontsize=18)
    plt.ylabel("Normalized Avg. Signal", fontsize=18)
    plt.title(f"{chip_name}", fontsize=22, weight="bold")
    plt.legend(frameon=False, fontsize=16, ncol=2)
    plt.xlim(-260, 260)
    plt.xticks([-250, -150, -50, 0, 50, 150, 250], fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(
        f"avg_{org.lower()}_{chip_name.lower()}_{res}_chr{chr}_{EXPAND_FACTOR}.png",
        dpi=300, bbox_inches="tight"
    )
    plt.close()


def cal_us_ds_signals(css, b_start, b_end, res, index_vals, signal_df, algo):
    signals = css[(css["start"] >= b_start) & (css["end"] <= b_end)]
    total_signal = signals["signal_value"].sum()
    signal_df.loc[0, algo] += total_signal

    ds_idx = 0
    ds_bp_lim = max(0, b_start-(res*(len(index_vals)//2)))
    for ds_bp in range(b_start, ds_bp_lim, -res):
        ds_start = max(0, ds_bp - res)
        ds_end = ds_bp
        signals = css[(css["start"] >= ds_start) & (css["end"] <= ds_end)]
        total_signal = signals["signal_value"].sum()
        ds_idx = ds_idx-res//1000
        signal_df.loc[ds_idx, algo] += total_signal

    us_idx = 0
    us_bp_lim = min(max_chr_bp, b_end+(res*(len(index_vals)//2)))
    for us_bp in range(b_end, us_bp_lim, res):
        us_start = us_bp
        us_end = max(0, us_bp + res)
        signals = css[(css["start"] >= us_start) & (css["end"] <= us_end)]
        total_signal = signals["signal_value"].sum()
        us_idx = us_idx+res//1000
        signal_df.loc[us_idx, algo] += total_signal


for org, chr, chip_filenames, chrom_size in zip(ORGANISMS, CHROMOSOMES, CHIP_SEQ_SIG_FILENAMES, CHROM_SIZES):
    org_ = org.lower()
    chr_ = f"chr{chr}"
    chrom_size_file = np.loadtxt(
        f"{CHIP_SEQ_SIG_PATH}/{org_}/{chrom_size}", delimiter="\t", dtype=str)
    max_chr_bp = chrom_size_file[chrom_size_file[:, 0]
                                 == f"{chr_}", 1].astype(int).item()
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
            for algo, filename in zip(ALGORITHMS, TAD_FILENAMES):
                bldf_idx = 0
                print(f"Algorithm: {algo}")
                tad_file = pd.read_csv(
                    f"{TAD_PATH}/{org_}/{org_}_10000_{chr_}_{filename}",
                    sep=",",
                    header=None,
                    names=TAD_COL_NAMES,
                    dtype=TAD_DTYPE_MAP
                )
                if algo == "Armatus":
                    tad_file["end"] += 1

                # b_start = 0
                # b_end = tad_file.iloc[0]["start"].astype(int)
                # middle = b_start + (b_end-b_start)//2
                # b_start = max(0, middle - expected_tb_region//2)
                # b_end = min(max_chr_bp, middle + expected_tb_region//2)
                # cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                #                   index_vals=index_vals, signal_df=signal_df, algo=algo)

                boundary_count = len(tad_file)
                for i in range(boundary_count):
                    middle = tad_file.iloc[i]["start"].astype(int)
                    b_start = max(0, middle - expected_tb_region//2)
                    b_end = min(max_chr_bp, middle + expected_tb_region//2)
                    cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                                      index_vals=index_vals, signal_df=signal_df, algo=algo)

                    middle = tad_file.iloc[i]["end"].astype(int)
                    b_start = max(0, middle - expected_tb_region//2)
                    b_end = min(max_chr_bp, middle + expected_tb_region//2)
                    cal_us_ds_signals(css=css, b_start=b_start, b_end=b_end, res=res,
                                      index_vals=index_vals, signal_df=signal_df, algo=algo)

                signal_df[algo] /= (boundary_count*2)
                # signal_df[algo] /= total_sv
                signal_df[algo] = np.log10(signal_df[algo])

            plot_signal_df(signal_df=signal_df, org=org, res=res, chr=chr, chip_name=chip_name,
                           normalize="zscore", smooth=True, gen_point=gen_point, shading=False, log=False)
