import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


nature_colors = ["#d55e00", "#009e74",   "#f0e442", "#0072b2",
                 "#56b3e9", "#e69f00",  "#cc79a7", "#000000"
                 ]

RESULT = "/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/simulated/results"
NOISES = [["4n_1", "4n_2", "4n_3", "4n_4", "4n_5"],
          ["8n_1", "8n_2", "8n_3", "8n_4", "8n_5"],
          ["12n_1", "12n_2", "12n_3", "12n_4", "12n_5"],
          ["16n_1", "16n_2", "16n_3", "16n_4", "16n_5"],
          ["20n_1", "20n_2", "20n_3", "20n_4", "20n_5"]]
TITLES = ["4 noise level", "8 noise level", "12 noise level",
          "16 noise level", "20 noise level"]
NOISE_NUM = [4, 8, 12, 16, 20]


def plot_size_distribution(dataset, title, filename):
    fig, axes = plt.subplots(figsize=(5, 6))
    sns.histplot(data=dataset, x="size", kde=True,
                 hue="TADs", palette=nature_colors)
    # axes.set_title(f"{title}")
    axes.set_xlabel("bp", fontsize=18)
    axes.set_ylabel("Frequency", fontsize=18)
    axes.tick_params(axis='x', labelsize=16)
    axes.tick_params(axis='y', labelsize=16)

    title = title.replace(" ", "_").lower()
    filename = f"{filename}_{title}"
    plt.savefig(
        f"/home/hc0783.unt.ad.unt.edu/workspace/codebase/EmbedTAD/analysis/{filename}.png", dpi=300, bbox_inches="tight")


overall = pd.DataFrame(columns=["TADs", "start", "end", "size"])
for noise_level, title in zip(NOISES, TITLES):
    dataframe = pd.DataFrame(columns=["TADs", "start", "end", "size"])
    for noise in noise_level:
        true_tads = pd.read_csv(
            f"{RESULT}/{noise}/TrueTAD.bed", sep=",", header=None, names=["start", "end"])
        caller_tads = pd.read_csv(
            f"{RESULT}/{noise}/EmbedTAD.bed", sep=",", header=None, names=["start", "end"])
        true_tads["TADs"] = "True"
        caller_tads["TADs"] = "EmbedTAD"
        true_tads["size"] = true_tads["end"] - true_tads["start"]
        caller_tads["size"] = caller_tads["end"] - caller_tads["start"]
        dataframe = pd.concat(
            [dataframe, true_tads, caller_tads], ignore_index=True)
        dataframe = dataframe[["TADs", "start", "end", "size"]]
    overall = pd.concat([overall, dataframe], ignore_index=True)
    overall = dataframe[["TADs", "start", "end", "size"]]

    plot_size_distribution(dataset=dataframe, title=title,
                           filename="insilicon_size_distribution")
plot_size_distribution(dataset=overall, title="Overall",
                       filename="insilicon_size_distribution")
