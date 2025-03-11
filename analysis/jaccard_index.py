import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# def calculate_JI(file1, file2):
#     size1 = os.path.getsize(file1)
#     size2 = os.path.getsize(file2)
#     if size1 == 0 or size2 == 0:
#         return 0
#     tads_1 = pd.read_csv(file1, sep=',', header=None)
#     tads_2 = pd.read_csv(file2, sep=',', header=None)
#     rep1 = set(tads_1[0]) | set(tads_1[1])
#     rep2 = set(tads_2[0]) | set(tads_2[1])
#     intersectsize = len(set(rep1) & set(rep2))
#     unionsize = len(set(rep1) | set(rep2))
#     return intersectsize / unionsize


# BASEPATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/comparison"
# ORGANISMS = ["gm12878", "ch12lx"]
# FILENAMES = ['Armatus', 'Caspian', 'ClusterTAD',
#              'EmbedTAD', 'HiCseg', 'IC_Finder', 'Spectral', 'TopDom']
# ALGORITHMS = ['Armatus', 'Caspian', 'ClusterTAD',
#               'EmbedTAD', 'HiCseg', 'IC Finder', 'Spectral', 'TopDom']
# RESOLUTIONS = ["5K", "10K"]

# for organism in ORGANISMS:
#     ji_df = pd.DataFrame(columns=['resolution', 'caller', 'number'])
#     for res in RESOLUTIONS:
#         for filename, algorithm in zip(FILENAMES, ALGORITHMS):
#             tad_1 = f"{BASEPATH}/{organism}/{res}/{filename}.bed"
#             for filename_1 in FILENAMES:
#                 if filename != filename_1:
#                     tad_2 = f"{BASEPATH}/{organism}/{res}/{filename_1}.bed"
#                     ji = calculate_JI(tad_1, tad_2)
#                     ji_df = ji_df._append({'resolution': res+'b', 'caller': algorithm, 'number': ji},
#                                           ignore_index=True)

#     plt.close('all')
#     fig = plt.subplots(figsize=(7, 4))
#     ax = plt.subplot(1, 1, 1)
#     sn.boxplot(x='caller', y='number', hue='resolution',
#                data=ji_df, ax=ax, showfliers=False)
#     sn.despine()
#     ax.set_ylabel('Jaccard Index')
#     ax.set_xlabel('')
#     for tick in ax.get_xticklabels():
#         tick.set_rotation(30)
#     ax.text(-0.08, 1.0, 'C', transform=ax.transAxes,
#             fontdict={'size': 22, 'color': 'black'})
#     ax.legend_.remove()
#     for tick in ax.get_xticklabels():
#         tick.set_rotation(30)

#     plt.title(f"{organism.upper()} ({res}b)", fontsize=16)
#     plt.xticks(fontsize=14)
#     plt.ylabel('Jaccard Index', fontsize=14)
#     plt.tight_layout()
#     plt.savefig(f"{organism}_boxplot_ji.png", dpi=300, bbox_inches='tight')


RESULT = "/home/mohit/Documents/project/embed_tad/data/simulated/results"
RESULT_FILES = ["TrueTAD", "EmbedTAD",   "ClusterTAD", "IC_Finder", "Caspian", "TopDom", "Armatus",
                "HiCSeg",  "Spectral"]

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


def calculate_JI(tads_1, tads_2):
    rep1 = set(tads_1[0]) | set(tads_1[1])
    rep2 = set(tads_2[0]) | set(tads_2[1])
    intersectsize = len(set(rep1) & set(rep2))
    unionsize = len(set(rep1) | set(rep2))
    return intersectsize / unionsize


def draw_boxplot(dataframe, title):
    filename_prefix = title.replace(" ", "_")
    dataframe.to_csv(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename_prefix}_jaccard_index.csv", index=False)
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 8))
    sns.boxplot(x='caller', y='ji', data=dataframe,
                hue="caller", showfliers=False)
    medians = dataframe.groupby("caller")["ji"].median()

    for i, caller in enumerate(medians.index):
        plt.text(i, medians[RESULT_FILES[i+1]], f'{medians[RESULT_FILES[i+1]]:.3f}',
                 ha='center', va='bottom', color="black")

    plt.xticks(rotation=65, labels=ALGORITHMS,
               ticks=np.arange(0, len(ALGORITHMS), 1))
    plt.xlabel("Caller")
    plt.ylabel("Jaccard Index")
    plt.title(f"{title}")
    plt.tight_layout()

    plt.savefig(
        f"/home/mohit/Documents/project/embed_tad/plots/{filename_prefix}_boxplot_jaccard_index.png", dpi=600, bbox_inches='tight')


ji_overall = pd.DataFrame(columns=['noise', 'caller', 'ji'])
for noise_level, title in zip(NOISES, TITLES):
    ji_df = pd.DataFrame(columns=['noise', 'caller', 'ji'])
    for noise in noise_level:
        tad_1 = f"{RESULT}/{noise}/TrueTAD.bed"
        tads_1 = pd.read_csv(tad_1, sep=',', header=None)
        for i in range(1, len(RESULT_FILES)):
            tad_2 = f"{RESULT}/{noise}/{RESULT_FILES[i]}.bed"
            tads_2 = pd.read_csv(tad_2, sep=',', header=None)
            ji = calculate_JI(tads_1, tads_2)
            ji_df = ji_df._append({'noise': noise, 'caller': RESULT_FILES[i], 'ji': ji},
                                  ignore_index=True)
            ji_overall = ji_overall._append({'noise': noise, 'caller': RESULT_FILES[i], 'ji': ji},
                                            ignore_index=True)
    # print(ji_df)
    draw_boxplot(ji_df, title)
draw_boxplot(ji_overall, "Overall Jaccard Index")
