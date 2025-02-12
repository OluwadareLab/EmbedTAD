import pandas as pd
from matplotlib_venn import venn3, venn3_circles
import matplotlib.pyplot as plt


def find_overlaps(dataset1, dataset2):
    overlaps = []
    for _, row1 in dataset1.iterrows():
        overlap = dataset2[(dataset2["start"] == row1["start"]) & (dataset2["end"] == row1["end"])]
        if not overlap.empty:
            overlaps.append(f"{row1['start']}-{row1['end']}")
    return set(overlaps)


def main():
    dataset1 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset2 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset3 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])

    overlaps_1_2 = find_overlaps(dataset1, dataset2)
    overlaps_1_3 = find_overlaps(dataset1, dataset3)
    overlaps_2_3 = find_overlaps(dataset2, dataset3)

    only_1 = len(set(dataset1["start"].astype(
        str) + "-" + dataset1["end"].astype(str)) - overlaps_1_2 - overlaps_1_3)
    only_2 = len(set(dataset2["start"].astype(
        str) + "-" + dataset2["end"].astype(str)) - overlaps_1_2 - overlaps_2_3)
    only_3 = len(set(dataset3["start"].astype(
        str) + "-" + dataset3["end"].astype(str)) - overlaps_1_3 - overlaps_2_3)
    shared_12 = len(overlaps_1_2 - overlaps_1_3 - overlaps_2_3)
    shared_13 = len(overlaps_1_3 - overlaps_1_2 - overlaps_2_3)
    shared_23 = len(overlaps_2_3 - overlaps_1_2 - overlaps_1_3)
    shared_all = len(overlaps_1_2 & overlaps_1_3 & overlaps_2_3)

    venn = venn3(subsets=(only_1, only_2, shared_12, only_3, shared_13, shared_23, shared_all),
                 set_labels=("Naive", "Th17", "Th1"),
        normalize_to=1.0  # Forces uniform scaling
    )

    # Draw circles manually with equal radii
    venn3_circles(subsets=(1, 1, 1, 1, 1, 1, 1), linestyle='solid', linewidth=2)

    # Adjust labels and subset text for visibility
    for label in venn.set_labels:
        if label:
            label.set_fontsize(14)

    for subset in venn.subset_labels:
        if subset:
            subset.set_fontsize(12)
    plt.title("Overlap")
    plt.savefig("/home/mohit/Documents/project/embed_tad/plots/mus_diagram.png",
                dpi=600, bbox_inches="tight")


def test():
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    dataset1 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset2 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])
    dataset3 = pd.read_csv("/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr2.txt",
                           sep="\t", header=None, names=["start", "end"])

    overlaps_1_2 = find_overlaps(dataset1, dataset2)
    print(f"Naive ∩ Th17: {len(overlaps_1_2)}")
    overlaps_1_3 = find_overlaps(dataset1, dataset3)
    print(f"Naive ∩ Th1: {len(overlaps_1_3)}")
    overlaps_2_3 = find_overlaps(dataset2, dataset3)
    print(f"Th17 ∩ Th1: {len(overlaps_2_3)}")

    only_1 = len(set(dataset1["start"].astype(
        str) + "-" + dataset1["end"].astype(str)) - overlaps_1_2 - overlaps_1_3) # Only Naive
    print(f"Only Naive: {only_1}")
    only_2 = len(set(dataset2["start"].astype(
        str) + "-" + dataset2["end"].astype(str)) - overlaps_1_2 - overlaps_2_3) # Only Th17
    print(f"Only Th17: {only_2}")
    only_3 = len(set(dataset3["start"].astype(
        str) + "-" + dataset3["end"].astype(str)) - overlaps_1_3 - overlaps_2_3) # Only Th1
    print(f"Only Th1: {only_3}")
    shared_12 = len(overlaps_1_2 - overlaps_1_3 - overlaps_2_3)
    print(f"Naive ∩ Th17: {shared_12}")
    shared_13 = len(overlaps_1_3 - overlaps_1_2 - overlaps_2_3)
    print(f"Naive ∩ Th1: {shared_13}")
    shared_23 = len(overlaps_2_3 - overlaps_1_2 - overlaps_1_3)
    print(f"Th17 ∩ Th1: {shared_23}")
    
    shared_all = len(overlaps_1_2 & overlaps_1_3 & overlaps_2_3)
    print(f"Naive ∩ Th17 ∩ Th1: {shared_all}")

    fig, ax = plt.subplots(figsize=(6, 6))
    radius = 0.3
    positions = [(0.5, 0.68), (0.65, 0.40), (0.32, 0.5)]

    colors = ['red', 'blue', 'green']
    # labels = ["Naive", "Th17", "Th1"]

    for pos, color in zip(positions, colors):
        circle = Circle(pos, radius, alpha=0.5, color=color)
        ax.add_patch(circle)

    # Set labels for sets
    ax.text(0.15, 0.12, "Naive", fontsize=14, color="black")
    ax.text(0.8, 0.05, "Th17", fontsize=14, color="black")
    ax.text(0.75, 0.95, "Th1", fontsize=14, color="black")

    # Position subset counts in appropriate locations
    ax.text(0.16, 0.40, str(only_1), fontsize=12, color="black")  # Only Naive
    ax.text(0.70, 0.25, str(only_2), fontsize=12, color="black")  # Only Th17
    ax.text(0.48, 0.85, str(only_3), fontsize=12, color="black")   # Only Th1

    ax.text(0.41, 0.30, str(shared_12), fontsize=12, color="black")  # Naive ∩ Th17
    ax.text(0.32, 0.65, str(shared_13), fontsize=12, color="black")  # Naive ∩ Th1
    ax.text(0.64, 0.58, str(shared_23), fontsize=12, color="black") # Th17 ∩ Th1

    ax.text(0.46, 0.49, str(shared_all), fontsize=14, color="black", fontweight="bold")  # Naive ∩ Th17 ∩ Th1 (center)

    # Customize axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.title("Overlap", fontsize=16)
    plt.savefig("/home/mohit/Documents/project/embed_tad/plots/mus_overlap_venn_diagram.png",
                dpi=600, bbox_inches="tight")

if __name__ == "__main__":
    test()
