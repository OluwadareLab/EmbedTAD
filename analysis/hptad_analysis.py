import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# EMBEDTAD_BASEPATH = "/home/mohit/Documents/project/embed_tad/data/results/gpu/mesc_gse35156"
# HPTAD_BASEPATH = "/home/mohit/Documents/project/HPTAD/data/result"
# RESOLUTION = 40000
# WINDOW = 0

# output = pd.DataFrame(columns=["chr", "percent"])
# for chr in range(1, 20):
#     count = 0
#     hptad_fn = f"{HPTAD_BASEPATH}/foo.HPTAD.chr{chr}.40000.tads.bed"
#     hptad = pd.read_csv(hptad_fn, sep="\t", header=None)
#     embedtad_fn = f"{EMBEDTAD_BASEPATH}/mesc_ori_40000_chr{chr}.txt"
#     embedtad = pd.read_csv(embedtad_fn, sep="\t", header=None)
#     total = len(embedtad)

#     for e_idx, e_row in embedtad.iterrows():
#         for h_idx, h_row in hptad.iterrows():
#             found = False
#             if e_row[0]-h_row[1] == 0:
#                 found = True
#             elif abs(e_row[0]-h_row[1]) < WINDOW or (e_row[0] > h_row[1] and e_row[0] < h_row[2]):
#                 found = True
#             else:
#                 found = False

#             if h_row[2]-e_row[1] == 0:
#                 found = found and True
#             elif abs(h_row[2]-e_row[1]) < WINDOW or (e_row[1] > h_row[1] and e_row[1] < h_row[2]):
#                 found = found and True
#             else:
#                 found = False

#             if found:
#                 count += 1
#                 break

#     percent = "{:.2f}".format((count/total)*100)
#     output.loc[len(output)] = [chr, percent]

# output.to_csv("/home/mohit/Documents/project/embed_tad/plots/hptad_recovery.csv", index=False)
data = {
    "chr": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "percent": [72.15,
                70.79,
                69.14,
                70.35,
                68.48,
                74.65,
                64.71,
                63.69,
                63.01,
                64.44,
                57.89,
                66.10,
                67.22,
                58.70,
                0.00,
                73.68,
                58.82,
                0.00,
                68.67]
}

nature_colors = ["#009e74",  "#0072b2",  "#f0e442", "#d55e00",
                 "#56b3e9", "#e69f00",  "#cc79a7", "#000000"
                 ]
df = pd.DataFrame(data)
plt.figure(figsize=(12, 4))
sns.barplot(data=df, x="chr", y="percent", color="#009e74")

# Add labels and title
plt.xlabel("Chromosome", fontsize=14)
plt.ylabel("Percentage (%)", fontsize=14)
plt.title("PLAC-seq TAD Recovery", fontsize=16)
plt.tight_layout()
plt.savefig(f"/home/hc0783.unt.ad.unt.edu/workspace/codebase/EmbedTAD/analysis/hptad_recovery.png",
            dpi=300, bbox_inches="tight")
