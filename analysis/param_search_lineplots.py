import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import matplotlib.ticker as ticker


def read_data(file):
    tad_qualities = pd.read_csv(file)
    overall = tad_qualities.groupby("dimension")[
        "MoC"].mean().round(2).reset_index()
    noise_4 = tad_qualities.query("noise==4").groupby(
        "dimension")["MoC"].mean().round(2).reset_index()
    noise_8 = tad_qualities.query("noise==8").groupby(
        "dimension")["MoC"].mean().round(2).reset_index()
    noise_12 = tad_qualities.query("noise==12").groupby(
        "dimension")["MoC"].mean().round(2).reset_index()
    noise_16 = tad_qualities.query("noise==16").groupby(
        "dimension")["MoC"].mean().round(2).reset_index()
    noise_20 = tad_qualities.query("noise==20").groupby(
        "dimension")["MoC"].mean().round(2).reset_index()

    return overall, noise_4, noise_8, noise_12, noise_16, noise_20


overall, n_4, n_8, n_12, n_16, n_20 = read_data(
    "/home/mohit/Documents/project/tad/codebase/analysis_results/param_search/netmf/Param_NetMF_score.csv")

colors = sns.color_palette(palette="rocket", n_colors=6, as_cmap=False)
palette = itertools.cycle(colors)
titles = ["Overall", "4 noise level", "8 noise level",
          "12 noise level", "16 noise level", "20 noise level"]

plt.rcParams.update({'font.size': 22})
fig, axes = plt.subplots(2, 3, figsize=(30, 20))
for ax, data, title in zip(axes.flat, [overall, n_4, n_8, n_12, n_16, n_20], titles):
    bars = sns.lineplot(data=data, x="dimension", y="MoC",
                        color=next(palette), linewidth=4,  ax=ax)
    ax.set_xlabel("Embedding Size")
    ax.set_ylabel("MoC")
    ax.set_title(title, fontsize=28)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
    ax.axvline(x=455, color='green', linestyle='--')
    ax.text(455, 0.20, '455', color='r', ha='right', va='top', rotation=90,
            transform=ax.get_xaxis_transform())

plt.savefig("param_search_lineplots.png", dpi=300, bbox_inches="tight")
