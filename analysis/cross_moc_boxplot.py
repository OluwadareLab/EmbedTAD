import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tad_scores import *

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"
ORGANISMS = ["GM12878", "CH12LX"]
CHROMOSOMES = [19, 18]
RESOLUTIONS = [5000, 10000]
CHR_SIZE_FILES = ["hg19.chrom.sizes", "mm9.chrom.sizes"]
TAD_FILENAMES = ["EmbedTAD.bed", "ClusterTAD.bed", "HiCseg.bed",
                 "Spectral.bed", "TopDom.bed", "Armatus.bed", "IC_Finder.bed", "Caspian.bed"]
PEAK_FILENAMES = [["wgEncodeBroadHistoneGm12878CtcfStdPk.txt",
                   "wgEncodeBroadHistoneGm12878H3k27acStdPk.txt",
                   "wgEncodeBroadHistoneGm12878H3k27me3StdPkV2.txt",
                   "wgEncodeBroadHistoneGm12878H3k4me1StdPk.txt",
                   "wgEncodeBroadHistoneGm12878H3k4me3StdPk.txt",
                   "wgEncodeBroadHistoneGm12878H3k9me3StdPk.txt",
                   "wgEncodeOpenChromChipGm12878Pol2Pk.txt"],
                  ["wgEncodeLicrHistoneCh12H3k27acFImmortalC57bl6StdPk.txt",
                      "wgEncodeLicrHistoneCh12H3k36me3FImmortalC57bl6StdPk.txt",
                      "wgEncodePsuHistoneCh12H3k27me3FImmortal2a4bInputPk.txt",
                      "wgEncodePsuTfbsCh12CtcfFImmortal2a4bInputPk.txt",
                      "wgEncodeSydhHistCh12H3k4me3IggyalePk.txt",
                      "wgEncodeSydhTfbsCh12Pol2IggmusPk.txt"]]
LABELS = [["CTCF", "H3k27ac", "H3k27me3", "H3k4me1", "H3k4me3", "H3k9me3",
           "Pol2"], ["H3k27ac", "H3k36me3", "H3k27me3", "Ctcf", "H3k4me3", "Pol2"]]
ALGORITHMS = ["EmbedTAD", "ClusterTAD", "HiCseg",
              "Spectral", "TopDom", "Armatus", "IC-Finder", "Caspian"]
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


def main():
    for organism, chr in zip(ORGANISMS, CHROMOSOMES):
        print(f"Organism: {organism}")
        ref_folder = organism.lower()
        for resol in RESOLUTIONS:
            print(f"Resolution: {resol}")
            res = "10K" if resol == 10000 else "5K"
            schema = {'resolution': 'str',
                      'algorithm': 'str', 'value': 'float64'}
            moc_df = pd.DataFrame(columns=schema.keys()).astype(schema)
            plt.rcParams.update({'font.size': 12})
            for tad_filename, algo in zip(TAD_FILENAMES, ALGORITHMS):
                print(f"Reference: {tad_filename}")
                tad_file = f"{BASE_PATH}/resutls/comparison/{ref_folder}/{res}/{tad_filename}"
                tads = pd.read_csv(tad_file, delimiter=",", header=None)
                for true_filename in TAD_FILENAMES:
                    if tad_filename != true_filename:
                        print(f"True: {true_filename}")
                        ttad_file = f"{BASE_PATH}/resutls/comparison/{ref_folder}/{res}/{true_filename}"
                        ttads = pd.read_csv(
                            ttad_file, delimiter=",", header=None)
                        try:
                            new_row = pd.DataFrame(
                                [[res+"b", algo, get_moc(tads=tads, true_tads=ttads)]], 
                                columns=moc_df.columns  # Ensure column names are matched
                            )

                            # Concatenate the new row to moc_df
                            moc_df = pd.concat([moc_df, new_row], ignore_index=True)
                        except Exception as e:
                            print(f"{e}")
                            continue

            plt.figure(figsize=(9, 5))
            sns.boxplot(data=moc_df, x="algorithm",
                        y="value", fill=False, gap=.1)
            plt.title(f"{organism} chr{chr} at {res}b")
            plt.xlabel(f"Algorithm")
            plt.ylabel(f"MoC")
            print(
                f"Saving figure {BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_cross_moc_boxplot.png")
            plt.savefig(f"{BASE_PATH}/resutls/comparison/plots/{organism}_{res}_chr{chr}_cross_moc_boxplot.png",
                        dpi=300, bbox_inches="tight")
            plt.close()


if __name__ == "__main__":
    main()
