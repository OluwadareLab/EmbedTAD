import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
palette = ["#0000FF", "#00FF00", "#FF0000", "#00FFFF", "#FF00FF"]
color_palette = sns.color_palette(palette)


def draw_quality_plot(dataframe, metric):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 3))
    box_plot = sns.barplot(x="Noise Level", y=metric, hue="Data",
                           data=dataframe, ci=None, legend=False, palette=color_palette)
    plt.xlabel("Noise Level")
    plt.ylabel(f"{metric}")
    plt.tight_layout()
    filename =  metric.replace(" ", "_").lower()
    plt.savefig(f"/home/mohit/Documents/project/embed_tad/plots/insilico_{filename}_barplot.png",
                dpi=600, bbox_inches='tight')


dataframe = pd.read_csv(
    "/home/mohit/Documents/project/embed_tad/EmbedTAD/analysis/cluster_quality.csv")

draw_quality_plot(dataframe, "TAD Quality")
draw_quality_plot(dataframe, "Silhouette Index")
draw_quality_plot(dataframe, "Davies Bouldin Index")
draw_quality_plot(dataframe, "Calinski Harabasz Index")
