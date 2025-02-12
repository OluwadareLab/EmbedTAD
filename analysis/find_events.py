import pandas as pd

def main(ref, data):
    dataset1 = pd.read_csv(ref, sep="\t", header=None, names=["start", "end"])
    dataset2 = pd.read_csv(data, sep="\t", header=None, names=["start", "end"])
    window = 100
    split_dict = {}
    split_events = 0
    for i in range(len(dataset1)):
        s1 = dataset1.iloc[i]["start"] - window
        e1 = dataset1.iloc[i]["end"] + window
        split_dict[(s1, e1)] = []
        for j in range(len(dataset2)):
            s2 = dataset2.iloc[j]["start"]
            e2 = dataset2.iloc[j]["end"]
            if s2 <= e1 and s2 >= s1 and e2 <= e1:
                split_dict[(s1, e1)].append((s2, e2))
            if s2 > e1:
                break
        if len(split_dict[(s1, e1)]) > 1:
            split_events += 1

    merge_dict = {}
    merge_events = 0
    for i in range(len(dataset2)):
        s1 = dataset2.iloc[i]["start"] - window
        e1 = dataset2.iloc[i]["end"] + window
        merge_dict[(s1, e1)] = []
        for j in range(len(dataset1)):
            s2 = dataset1.iloc[j]["start"]
            e2 = dataset1.iloc[j]["end"]
            if s2 <= e1 and s2 >= s1 and e2 <= e1:
                merge_dict[(s1, e1)].append((s2, e2))
            if s2 > e1:
                break
        if len(merge_dict[(s1, e1)]) > 1:
            merge_events += 1
    print(f"Split events: {split_events}, Merge events: {merge_events}")


if __name__ == "__main__":
    ref = "/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr2.txt"
    data = "/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr2.txt"
    print("Naive vs Th17")
    main(ref=ref, data=data)
    print("Naive vs Th1")
    data = "/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr2.txt"
    main(ref=ref, data=data)

