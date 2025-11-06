import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_size_distribution(dataset1, dataset2, dataset3):
    dataset1["size"] = dataset1["end"] - dataset1["start"]
    dataset2["size"] = dataset2["end"] - dataset2["start"]
    dataset3["size"] = dataset3["end"] - dataset3["start"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 5))
    sns.histplot(dataset1["size"], label="Naïve",
                 kde=True, ax=axes[0], color="#e69f00")
    axes[0].set_title("Naïve")
    axes[0].set_ylabel("Frequency")
    axes[0].set_xlabel("bp")
    # axes[0].legend()

    sns.histplot(dataset2["size"], label="Th17",
                 kde=True, ax=axes[1], color="#56b3e9")
    axes[1].set_title("Th17")
    axes[1].set_ylabel("Frequency")
    axes[1].set_xlabel("bp")
    # axes[1].legend()

    sns.histplot(dataset3["size"], label="Th1",
                 kde=True, ax=axes[2], color="#009e74")
    axes[2].set_title("Th1")
    axes[2].set_ylabel("Frequency")
    axes[2].set_xlabel("bp")
    # axes[2].legend()

    fig.suptitle("Size Distribution")
    plt.savefig("/home/hc0783.unt.ad.unt.edu/workspace/codebase/EmbedTAD/analysis/mus_size_distribution.png",
                dpi=300, bbox_inches="tight")


def main():
    dataset1 = pd.read_csv("/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/gpu/mus_gse210418/naive_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset2 = pd.read_csv("/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/gpu/mus_gse210418/th17_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset3 = pd.read_csv("/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/gpu/mus_gse210418/th1_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])

    plot_size_distribution(dataset1, dataset2, dataset3)


if __name__ == "__main__":
    main()
