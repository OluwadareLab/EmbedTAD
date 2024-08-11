import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_heatmap(matrix, tad_regions, file, figure_size=(12, 12), dpi=200):
    _, ax = plt.subplots(figsize=figure_size)
    ax = sns.heatmap(matrix, yticklabels=False,
                     xticklabels=False, cbar=False, cmap="YlOrBr")
    for _, row in tad_regions.iterrows():
        ax.add_patch(patches.Rectangle(
            (row["start"], row["start"]), row["count"], row["count"], fill=False, edgecolor="blue", lw=1))

    plt.savefig(file + "_heatmap.png",
                dpi=dpi, bbox_inches="tight")


def draw_heatmap_area(matrix, tad_regions, file, first_tad_count=30, figure_size=(12, 12), dpi=200):
    pass
    _, ax = plt.subplots(figsize=figure_size)
    lim = min(tad_regions.shape[0], first_tad_count)
    if lim > 0:
        regions = tad_regions.head(lim)
        ax = sns.heatmap(matrix[:regions.loc[lim-1].at["end"], :regions.loc[lim-1].at["end"]], yticklabels=False,
                         xticklabels=False, cbar=False, cmap="YlOrBr")
        for _, row in regions.iterrows():
            ax.add_patch(patches.Rectangle(
                (row["start"], row["start"]), row["count"], row["count"], fill=False, edgecolor="blue", lw=1))

        plt.savefig(file + "_" + str(first_tad_count) + "_heatmap.png",
                    dpi=dpi, bbox_inches="tight")