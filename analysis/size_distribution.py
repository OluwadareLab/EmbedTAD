import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_size_distribution(dataset1, dataset2, dataset3):
    dataset1["size"] = dataset1["end"] - dataset1["start"]
    dataset2["size"] = dataset2["end"] - dataset2["start"]
    dataset3["size"] = dataset3["end"] - dataset3["start"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 5))
    sns.histplot(dataset1["size"], label="Naive", kde=True, ax=axes[0], color="blue")
    axes[0].set_title("Naive")
    axes[0].set_ylabel("Frequency")
    axes[0].set_xlabel("bp")
    # axes[0].legend()

    sns.histplot(dataset2["size"], label="Th17", kde=True, ax=axes[1], color="green")
    axes[1].set_title("Th17")
    axes[1].set_ylabel("Frequency")
    axes[1].set_xlabel("bp")
    # axes[1].legend()

    sns.histplot(dataset3["size"], label="Th1", kde=True, ax=axes[2], color="red")
    axes[2].set_title("Th1")
    axes[2].set_ylabel("Frequency")
    axes[2].set_xlabel("bp")
    # axes[2].legend()

    fig.suptitle("Size Distribution")
    plt.savefig("size_distribution.png", dpi=600, bbox_inches="tight")

def main():
    dataset1 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_naiev_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset2 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th17_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset3 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th1_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])

    plot_size_distribution(dataset1, dataset2, dataset3)

if __name__ == "__main__":
    main()