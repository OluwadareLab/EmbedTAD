import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


RESULT = "/home/mohit/Documents/project/embed_tad/data/simulated/results"
NOISES = [["4n_1", "4n_2", "4n_3", "4n_4", "4n_5"],
          ["8n_1", "8n_2", "8n_3", "8n_4", "8n_5"],
          ["12n_1", "12n_2", "12n_3", "12n_4", "12n_5"],
          ["16n_1", "16n_2", "16n_3", "16n_4", "16n_5"],
          ["20n_1", "20n_2", "20n_3", "20n_4", "20n_5"]]
TITLES = ["4 noise level", "8 noise level", "12 noise level",
          "16 noise level", "20 noise level"]
NOISE_NUM = [4, 8, 12, 16, 20]


def draw_boxplot(dataframe, metric, title, filename):
    filename = filename.replace(" ", "_")
    dataframe.to_csv(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename}.csv", index=False)
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 8))
    box_plot = sns.boxplot(x='noise', y=metric, data=dataframe,
                           hue="TADs", showfliers=False, ax=ax)

    medians = dataframe.groupby(["noise", "TADs"])[
        metric].median().reset_index()

    hue_levels = dataframe["TADs"].unique()
    positions = {category: idx for idx,
                 category in enumerate(hue_levels)}

    for i, row in medians.iterrows():
        noise_level = row["noise"]
        tad_group = row["TADs"]
        median_value = row[metric]

        x_base = np.where(np.array(NOISE_NUM) == noise_level)[
            0][0]
        hue_offset = (positions[tad_group] - (len(hue_levels) - 1) / 2) * 0.4

        plt.text(
            x_base + hue_offset,
            median_value,
            f'{median_value:.0f}',
            ha='center', va='bottom', color="black", fontweight='bold'
        )

    plt.xticks(rotation=0, labels=NOISE_NUM,
               ticks=np.arange(0, len(NOISE_NUM), 1))

    plt.xlabel("Noise Level")
    plt.ylabel("Count")
    # plt.title(f"{title}")
    plt.tight_layout()

    plt.savefig(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename}_boxplot.png", dpi=600, bbox_inches='tight')


overall_score = pd.DataFrame(
    columns=["TADs", "noise", "n_tads"])
for noise_level, n in zip(NOISES, NOISE_NUM):
    for noise in noise_level:
        true_tads = pd.read_csv(
            f"{RESULT}/{noise}/TrueTAD.bed", sep=",", header=None)
        caller_tads = pd.read_csv(
            f"{RESULT}/{noise}/EmbedTAD.bed", sep=",", header=None)
        overall_score = overall_score._append(
            {"TADs": "True", "noise": n, "n_tads": len(true_tads)}, ignore_index=True)
        overall_score = overall_score._append(
            {"TADs": "EmbedTAD", "noise": n, "n_tads": len(caller_tads)}, ignore_index=True)

draw_boxplot(dataframe=overall_score, metric="n_tads",
             title="Number of TADs", filename="insilicon_number_of_tads")
