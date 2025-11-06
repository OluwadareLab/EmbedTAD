import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nature_colors = ["#009e74",  "#0072b2",  "#f0e442", "#d55e00",
                 "#56b3e9", "#e69f00",  "#cc79a7", "#000000"
                 ]
color_palette = sns.color_palette(nature_colors)


def draw_quality_plot(dataframe, metric):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 3))
    box_plot = sns.barplot(x="Noise Level", y=metric, hue="Data",
                           data=dataframe, ci=None, legend=False, palette=color_palette)
    plt.xlabel("Noise Level")
    plt.ylabel(f"{metric}")
    plt.tight_layout()
    filename = metric.replace(" ", "_").lower()
    plt.savefig(f"/home/hc0783.unt.ad.unt.edu/workspace/codebase/EmbedTAD/analysis/insilico_{filename}_barplot.png",
                dpi=300, bbox_inches='tight')


dataframe = pd.read_csv(
    "/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/EmbedTAD/analysis/cluster_quality.csv")

draw_quality_plot(dataframe, "TAD Quality")
draw_quality_plot(dataframe, "Silhouette Index")
draw_quality_plot(dataframe, "Davies Bouldin Index")
draw_quality_plot(dataframe, "Calinski Harabasz Index")
