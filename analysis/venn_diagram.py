import pandas as pd
from matplotlib_venn import venn3
import matplotlib.pyplot as plt

def find_overlaps(dataset1, dataset2):
    overlaps = []
    for _, row1 in dataset1.iterrows():
        overlap = dataset2[
            (dataset2["start"] <= row1["end"]) & (dataset2["end"] >= row1["start"])
        ]
        if not overlap.empty:
            overlaps.append(f"{row1['chrom']}:{row1['start']}-{row1['end']}")
    return set(overlaps)

def main():
    dataset1 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_naiev_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset2 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th17_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset3 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th1_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])

    overlaps_1_2 = find_overlaps(dataset1, dataset2)
    overlaps_1_3 = find_overlaps(dataset1, dataset3)
    overlaps_2_3 = find_overlaps(dataset2, dataset3)

    only_1 = len(set(dataset1["start"].astype(str) + "-" + dataset1["end"].astype(str)) - overlaps_1_2 - overlaps_1_3)
    only_2 = len(set(dataset2["start"].astype(str) + "-" + dataset2["end"].astype(str)) - overlaps_1_2 - overlaps_2_3)
    only_3 = len(set(dataset3["start"].astype(str) + "-" + dataset3["end"].astype(str)) - overlaps_1_3 - overlaps_2_3)
    shared_12 = len(overlaps_1_2 - overlaps_1_3 - overlaps_2_3)
    shared_13 = len(overlaps_1_3 - overlaps_1_2 - overlaps_2_3)
    shared_23 = len(overlaps_2_3 - overlaps_1_2 - overlaps_1_3)
    shared_all = len(overlaps_1_2 & overlaps_1_3 & overlaps_2_3)

    venn3(subsets=(only_1, only_2, shared_12, only_3, shared_13, shared_23, shared_all),
          set_labels=("Naive", "Th17", "Th1"))
    plt.title("Overlap of TADs")
    plt.savefig("venn_diagram.png", dpi=600, bbox_inches="tight")

if __name__ == "__main__":
    main()
