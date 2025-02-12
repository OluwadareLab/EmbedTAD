import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.simplefilter(action='ignore')



def draw_heatmap(matrix, tad_regions, file, figure_size=(12, 12), dpi=200):
    custom_cmap = LinearSegmentedColormap.from_list('interaction',
                                                      ['#FFFFFF', '#FFDFDF', '#FF7575', '#FF2626', '#F70000'])
    _, ax = plt.subplots(figsize=figure_size)
    ax = sns.heatmap(matrix, yticklabels=False,
                     xticklabels=False, cbar=False, cmap=custom_cmap)
    for _, row in tad_regions.iterrows():
        ax.add_patch(patches.Rectangle(
            (row["start"], row["start"]), row["count"], row["count"], fill=False, edgecolor="blue", lw=1))

    plt.savefig(file + "_heatmap.png",
                dpi=dpi, bbox_inches="tight")


def draw_heatmap_area(matrix, tad_regions, file, first_tad_count=30, figure_size=(12, 12), dpi=200):
    pass
    custom_cmap = LinearSegmentedColormap.from_list('interaction',
                                                      ['#FFFFFF', '#FFDFDF', '#FF7575', '#FF2626', '#F70000'])
    _, ax = plt.subplots(figsize=figure_size)
    lim = min(tad_regions.shape[0], first_tad_count)
    if lim > 0:
        regions = tad_regions.head(lim)
        ax = sns.heatmap(matrix[:regions.loc[lim-1].at["end"], :regions.loc[lim-1].at["end"]], yticklabels=False,
                         xticklabels=False, cbar=False, cmap=custom_cmap)
        for _, row in regions.iterrows():
            ax.add_patch(patches.Rectangle(
                (row["start"], row["start"]), row["count"], row["count"], fill=False, edgecolor="blue", lw=1))

        plt.savefig(file + "_" + str(first_tad_count) + "_heatmap.png",
                    dpi=dpi, bbox_inches="tight")


def draw_heatmap(matrix, figure_size=(12, 12), dpi=600):
    custom_cmap = LinearSegmentedColormap.from_list('interaction',
                                                      ['#FFFFFF', '#FFDFDF', '#FF7575', '#FF2626', '#F70000'])
    _, ax = plt.subplots(figsize=figure_size)
    ax = sns.heatmap(matrix[1650:1750, 1650:1750], yticklabels=False,
                     xticklabels=False, cbar=False, cmap=custom_cmap)

    plt.savefig("example_heatmap.png",
                dpi=dpi, bbox_inches="tight")

import numpy as np
if __name__:
    raw_matrix = np.loadtxt("/home/mohit/Documents/project/caspian/TAD_results/SimulationData/4noise.hic")
    draw_heatmap(raw_matrix)