import pandas as pd
import matplotlib.pyplot as plt

def plot_tad_counts(dataset1, dataset2, dataset3):
    count1 = len(dataset1)
    count2 = len(dataset2)
    count3 = len(dataset3)

    plt.figure(figsize=(3, 5))
    bars = plt.bar(["Naive", "Th17", "Th1"], [count1, count2, count3], color=["orange", "blue",  "red"], alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, f'{int(height)}', ha='center', va='bottom')

    plt.title("Number of TADs")
    plt.ylabel("Count")
    plt.savefig("number_of_tads.png", dpi=600, bbox_inches="tight")

def main():
    dataset1 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_naiev_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset2 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th17_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])
    dataset3 = pd.read_csv("/home/mohit/Documents/project/EmbedTAD/data/bio_analysis/mouse_th1_10000_chr2.bed", sep="\t", header=None, names=["chrom", "start", "end"])

    plot_tad_counts(dataset1, dataset2, dataset3)

if __name__ == "__main__":
    main()