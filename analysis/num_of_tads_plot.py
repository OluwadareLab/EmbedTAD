import pandas as pd
import matplotlib.pyplot as plt


def plot_tad_counts(count1, count2, count3):
    plt.figure(figsize=(3, 5))
    bars = plt.bar(["Naive", "Th17", "Th1"], [count1, count2, count3], color=[
                   "orange", "blue",  "red"], alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height,
                 f'{int(height)}', ha='center', va='bottom')

    plt.title("Number of TADs")
    plt.ylabel("Count")
    plt.savefig("/home/mohit/Documents/project/embed_tad/plots/mus_number_of_tads.png",
                dpi=600, bbox_inches="tight")


def main():
    count1 = 0
    count2 = 0
    count3 = 0
    for chr in range(1, 20):
        dataset1 = pd.read_csv(f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr{chr}.txt",
                               sep="\t", header=None, names=["start", "end"])
        dataset2 = pd.read_csv(f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr{chr}.txt",
                               sep="\t", header=None, names=["start", "end"])
        dataset3 = pd.read_csv(f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr{chr}.txt",
                               sep="\t", header=None, names=["start", "end"])
        count1 += len(dataset1)
        count2 += len(dataset2)
        count3 += len(dataset3)
    plot_tad_counts(count1, count2, count3)


if __name__ == "__main__":
    main()
