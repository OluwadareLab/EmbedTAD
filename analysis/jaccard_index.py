import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def calculate_JI(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    if size1 == 0 or size2 == 0:
        return 0
    tads_1 = pd.read_csv(file1, sep=',', header=None)
    tads_2 = pd.read_csv(file2, sep=',', header=None)
    rep1 = set(tads_1[0]) | set(tads_1[1])
    rep2 = set(tads_2[0]) | set(tads_2[1])
    intersectsize = len(set(rep1) & set(rep2))
    unionsize = len(set(rep1) | set(rep2))
    return intersectsize / unionsize


BASEPATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/comparison"
ORGANISMS = ["gm12878", "ch12lx"]
FILENAMES = ['Armatus', 'Caspian', 'ClusterTAD',
             'EmbedTAD', 'HiCseg', 'IC_Finder', 'Spectral', 'TopDom']
ALGORITHMS = ['Armatus', 'Caspian', 'ClusterTAD',
              'EmbedTAD', 'HiCseg', 'IC Finder', 'Spectral', 'TopDom']
RESOLUTIONS = ["5K", "10K"]

for organism in ORGANISMS:
    ji_df = pd.DataFrame(columns=['resolution', 'caller', 'number'])
    for res in RESOLUTIONS:
        for filename, algorithm in zip(FILENAMES, ALGORITHMS):
            tad_1 = f"{BASEPATH}/{organism}/{res}/{filename}.bed"
            for filename_1 in FILENAMES:
                if filename != filename_1:
                    tad_2 = f"{BASEPATH}/{organism}/{res}/{filename_1}.bed"
                    ji = calculate_JI(tad_1, tad_2)
                    ji_df = ji_df._append({'resolution': res+'b', 'caller': algorithm, 'number': ji},
                                          ignore_index=True)

    plt.close('all')
    fig = plt.subplots(figsize=(7, 4))
    ax = plt.subplot(1, 1, 1)
    sn.boxplot(x='caller', y='number', hue='resolution',
               data=ji_df, ax=ax, showfliers=False)
    sn.despine()
    ax.set_ylabel('Jaccard Index')
    ax.set_xlabel('')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    ax.text(-0.08, 1.0, 'C', transform=ax.transAxes,
            fontdict={'size': 22, 'color': 'black'})
    ax.legend_.remove()
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)

    plt.title(f"{organism.upper()} ({res}b)", fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel('Jaccard Index', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{organism}_boxplot_ji.png", dpi=300, bbox_inches='tight')
