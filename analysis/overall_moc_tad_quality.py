import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tad_scores import get_moc, get_tad_quality

RESULT = "/home/mohit/Documents/project/embed_tad/data/simulated/results"
RESULT_FILES = ["EmbedTAD_CPU", "ClusterTAD", "IC_Finder", "Caspian", "TopDom", "Armatus",
                "HiCSeg", "Spectral"]

NOISES = [["4n_1",
           "4n_2",
           "4n_3",
           "4n_4",
           "4n_5"],
          ["8n_1",
           "8n_2",
           "8n_3",
           "8n_4",
           "8n_5"],
          ["12n_1",
           "12n_2",
           "12n_3",
           "12n_4",
           "12n_5"],
          ["16n_1",
           "16n_2",
           "16n_3",
           "16n_4",
           "16n_5"],
          ["20n_1",
           "20n_2",
           "20n_3",
           "20n_4",
           "20n_5"]]
TITLES = ["4 noise level", "8 noise level", "12 noise level",
          "16 noise level", "20 noise level"]
ALGORITHMS = ["EmbedTAD",   "ClusterTAD", "IC Finder", "Caspian", "TopDom", "Armatus",
              "HiCSeg",  "Spectral"]


def draw_boxplot(dataframe, metric, title, filename):
    filename = filename.replace(" ", "_")
    dataframe.to_csv(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename}.csv", index=False)
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 8))
    sns.boxplot(x='caller', y=metric, data=dataframe,
                hue="caller", showfliers=False)
    medians = dataframe.groupby("caller")[metric].median()

    for i, caller in enumerate(medians.index):
        plt.text(i, medians[RESULT_FILES[i]], f'{medians[RESULT_FILES[i]]:.3f}',
                 ha='center', va='bottom', color="black")

    plt.xticks(rotation=65, labels=ALGORITHMS,
               ticks=np.arange(0, len(ALGORITHMS), 1))
    plt.xlabel("Caller")
    plt.ylabel("Jaccard Index")
    plt.title(f"{title}")
    plt.tight_layout()

    plt.savefig(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename}_boxplot.png", dpi=600, bbox_inches='tight')


overall_score = pd.DataFrame(columns=["noise", "caller", "moc", "tq", "n_tads"])
for noise_level, title in zip(NOISES, TITLES):
    single_noise_score = pd.DataFrame(columns=["noise", "caller", "moc", "tq", "n_tads"])
    for noise in noise_level:
        true_tads = pd.read_csv(
            f"{RESULT}/{noise}/TrueTAD.bed", sep=",", header=None)
        matrix = np.loadtxt(f"{RESULT}/{noise}/matrix.txt")
        for i in range(0, len(RESULT_FILES)):
            caller_tads = pd.read_csv(
                f"{RESULT}/{noise}/{RESULT_FILES[i]}.bed", sep=",", header=None)
            moc = 0
            # moc = get_moc(caller_tads, true_tads)
            tq = 0
            # tq = get_tad_quality(caller_tads.div(40000).astype('int').to_numpy(), matrix)
            single_noise_score = single_noise_score._append({"noise": noise, "caller": RESULT_FILES[i], "moc": moc, "tq": tq, "n_tads": len(caller_tads)},
                                                            ignore_index=True)
            overall_score = overall_score._append({"noise": noise, "caller": RESULT_FILES[i], "moc": moc, "tq": tq, "n_tads": len(caller_tads)},
                                                  ignore_index=True)
    # draw_boxplot(single_noise_score, "moc", title, f"moc_{title}")
    draw_boxplot(single_noise_score, "n_tads", title, f"n_tads_{title}")

# draw_boxplot(overall_score, "moc", "Overall", "moc_overall")
draw_boxplot(overall_score, "n_tads", "Overall", "n_tads_overall")