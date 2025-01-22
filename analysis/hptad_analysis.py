import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

EMBEDTAD_BASEPATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/raw/mesc"
HPTAD_BASEPATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/hptad"
RESOLUTION = 40000
WINDOW = 50

# output = pd.DataFrame(columns=["chr", "percent"])
# for chr in range(1, 20):
#     count = 0
#     hptad_fn = f"{HPTAD_BASEPATH}/foo.HPTAD.chr{chr}.40000.tads.bed"
#     hptad = pd.read_csv(hptad_fn, sep="\t", header=None)
#     embedtad_fn = f"{EMBEDTAD_BASEPATH}/mESC_40000_chr{chr}.bed"
#     embedtad = pd.read_csv(embedtad_fn, sep="\t", header=None)
#     total = len(embedtad)

#     for e_idx, e_row in embedtad.iterrows():
#         for h_idx, h_row in hptad.iterrows():
#             found = False
#             if e_row[1]-h_row[1] == 0:
#                 found = True
#             elif abs(e_row[1]-h_row[1]) < WINDOW or (e_row[1] > h_row[1] and e_row[1] < h_row[2]):
#                 found = True
#             else:
#                 found = False

#             if h_row[2]-e_row[3] == 0:
#                 found = found and True
#             elif abs(h_row[2]-e_row[3]) < WINDOW or (e_row[3] > h_row[1] and e_row[3] < h_row[2]):
#                 found = found and True
#             else:
#                 found = False

#             if found:
#                 count += 1
#                 break

#     percent = "{:.2f}".format((count/total)*100)
#     output.loc[len(output)] = [chr, percent]

# output.to_csv("hptad_recovery.csv", index=False)
data = {
    "chr": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "percent": [67.12,
                68.24,
                66.14,
                66.67,
                64.63,
                68.60,
                59.21,
                60.77,
                61.22, 57.14, 52.34, 60.66, 62.01, 56.03, 0.00, 68.39, 57.35, 0.00, 64.37]
}
df = pd.DataFrame(data)
plt.figure(figsize=(12, 4))
sns.barplot(data=df, x="chr", y="percent", palette="viridis")

# Add labels and title
plt.xlabel("Chromosome", fontsize=14)
plt.ylabel("Percentage (%)", fontsize=14)
plt.title("PLAC-seq TAD Recovery", fontsize=16)
plt.tight_layout()
plt.savefig(f"hptad_recovery.png", dpi=300, bbox_inches="tight")
