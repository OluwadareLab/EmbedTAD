import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import make_interp_spline


TAD_PATH = "/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/comparison"
TAD_FILENAMES = ["topdom.bed",
                 "hicseg.bed",
                 "spectral.bed",
                 "clustertad.bed",
                 "armatus.bed",
                 "ic_finder.bed",
                 "caspian.bed",
                 "embedtad.bed"]
ALGORITHMS = ["TopDom", "HiCSeg", "Spectral", "ClusterTAD",
              "Armatus", "IC-Finder", "Caspian", "EmbedTAD"]

RESOLUTIONS = [5000, 10000]
ORGANISMS = ["GM12878", "CH12LX"]
CHROMOSOMES = [19, 18]

TAD_COL_NAMES = ["start", "end"]
TAD_DTYPE_MAP = {
    "start": int,
    "end": int
}


def plot_tad_counts(data_df, filename):
    # Bar plot
    row = data_df.iloc[0]

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(row.index, row.values, color="skyblue", edgecolor="black")

    # Annotate counts at the top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2, height,
            f"{int(height):,}",   # add commas for readability
            ha="center", va="bottom", fontsize=10, weight="bold"
        )

    plt.ylabel("Count", fontsize=12)
    plt.xlabel("TAD Callers")
    plt.title("TAD Count", fontsize=14, weight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{filename}.png", dpi=600, bbox_inches="tight")
    plt.close()


def plot_boundary_type_counts(data_df, filename):
    df = data_df.copy()
    zero_counts = (df == 0).sum(skipna=True)
    nonzero_counts = (df > 0).sum(skipna=True)

    counts_df = pd.DataFrame({
        "Continuous": zero_counts,
        "Gap": nonzero_counts
    })

    ax = counts_df.plot(
        kind="bar",
        figsize=(12, 6),
        stacked=False,
        width=0.8
    )

    # Add text labels on bars
    for p in ax.patches:
        value = int(p.get_height())
        if value > 0:  # only annotate non-empty bars
            ax.annotate(
                str(value),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha="center", va="bottom",
                fontsize=10, fontweight="bold",
                xytext=(0, 3),  # small vertical offset
                textcoords="offset points"
            )

    plt.ylabel("Count")
    plt.xlabel("TAD Callers")
    plt.title("TAD Boundary Type Count",
              fontsize=14, weight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Type")
    plt.tight_layout()
    plt.savefig(f"{filename}.png", dpi=600, bbox_inches="tight")
    plt.close()


def plot_boundary_width_dist(data_df, filename):
    df = data_df.copy()
    df_nonzero = df[df > 0].dropna(how="all")
    df_long = df_nonzero.melt(var_name="Algorithm", value_name="Gap").dropna()

    plt.figure(figsize=(10, 8))
    # Full plot with outliers
    sns.boxplot(data=df_long, x="Algorithm", y="Gap", fill=False)

    plt.yscale("log")
    # plt.ylim(df_long["Gap"].quantile(0.05), df_long["Gap"].quantile(0.95))
    plt.ylabel("Boundary Width (bp)", fontsize=12)
    plt.xlabel("TAD Callers", fontsize=12)
    plt.title("Distribution of TAD Boundary (GAP)",
              fontsize=14, weight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{filename}.png", dpi=600, bbox_inches="tight")
    plt.close()

# def plot_boundary_width_dist(data_df, filename):
#     df = data_df.copy()
#     df_nonzero = df[df > 0].dropna(how="all")

#     # Melt to long format
#     df_long = df_nonzero.melt(var_name="Algorithm",
#                               value_name="Value").dropna()

#     # Compute statistics table
#     stats_df = df_long.groupby("Algorithm")["Value"].agg(
#         ["min", "median", "mean", "max"])
#     stats_df = stats_df.round(2)  # round for readability

#     # Save or display the table
#     print(stats_df)
#     stats_df.to_csv(f"{filename}.csv")  # optional save

#     # Boxplot with mean/median markers only
#     plt.figure(figsize=(12, 6))
#     sns.boxplot(data=df_long, x="Algorithm",
#                 y="Value", showfliers=False, width=0.6)

#     # Mean marker (red diamond)
#     sns.pointplot(data=df_long, x="Algorithm", y="Value",
#                   estimator="mean", color="red", join=False, markers="D")

#     # Median marker (blue triangle)
#     sns.pointplot(data=df_long, x="Algorithm", y="Value",
#                   estimator="median", color="blue", join=False, markers="^")

#     # Labels & title
#     plt.ylabel("Boundary Width", fontsize=12)
#     plt.xlabel("TAD Callers", fontsize=12)
#     plt.title("Distribution of TAD Boundary (GAP)",
#               fontsize=14, weight="bold")
#     plt.xticks(rotation=45, ha="right")

#     # Custom legend
#     from matplotlib.lines import Line2D
#     legend_elements = [
#         Line2D([0], [0], marker="D", color="red",
#                linestyle="None", markersize=8, label="Mean"),
#         Line2D([0], [0], marker="^", color="blue",
#                linestyle="None", markersize=8, label="Median"),
#     ]
#     plt.legend(handles=legend_elements, title="Statistics", frameon=False)

#     plt.tight_layout()
#     plt.savefig(f"{filename}.png", dpi=600, bbox_inches="tight")
#     plt.close()


for org, chr in zip(ORGANISMS, CHROMOSOMES):
    org_ = org.lower()
    chr_ = f"chr{chr}"
    max_chr_bp = 59128983
    for res in RESOLUTIONS:
        print(f"Organism: {org}, chromosome: {chr}, Resolution: {res}")
        boundary_len_df = pd.DataFrame(columns=ALGORITHMS)
        num_of_tad_df = pd.DataFrame(columns=ALGORITHMS)
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
            b_start = 0
            b_end = tad_file.iloc[0]["start"].astype(int)
            boundary_len = b_end - b_start
            boundary_len_df.loc[bldf_idx, algo] = boundary_len
            bldf_idx += 1

            # at middle
            tad_count = len(tad_file)
            num_of_tad_df.loc[0, algo] = tad_count
            boundary_count = tad_count - 1

            for i in range(boundary_count):
                current_row = tad_file.iloc[i]
                next_row = tad_file.iloc[i + 1]
                b_start = current_row["end"].astype(int)
                b_end = next_row["start"].astype(int)
                boundary_len = b_end - b_start
                boundary_len_df.loc[bldf_idx, algo] = boundary_len
                bldf_idx += 1

            # at end
            b_start = tad_file.iloc[-1]["end"].astype(int)
            b_end = max_chr_bp
            boundary_len = b_end - b_start
            boundary_len_df.loc[bldf_idx, algo] = boundary_len
            bldf_idx += 1
        boundary_len_df.to_csv(
            f"avg_{org.lower()}_{res}_chr{chr}.csv", index=False)
        plot_tad_counts(
            num_of_tad_df, filename=f"num_of_tad_count_{org.lower()}_{res}_chr{chr}")
        plot_boundary_type_counts(
            data_df=boundary_len_df, filename=f"boundary_type_count_{org.lower()}_{res}_chr{chr}")
        plot_boundary_width_dist(
            data_df=boundary_len_df, filename=f"boundary_width_dist_{org.lower()}_{res}_chr{chr}")
