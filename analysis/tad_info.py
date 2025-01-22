import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.ticker as ticker

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/raw"
ORGANISM = ["gm12878", "ch12lx"]
RESOLS = [[5000, 10000], [5000, 10000]]
CHROMS = [[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
          [2, 4, 6, 8, 10, 12, 14, 16, 18]]

OUTPUT_PATH = "/home/mohit/Documents/project/EmbedTAD/data/chip_sig/"


def add_annotations(ax, bars, fontsize=16):
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        fontweight = 'normal'
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f'{int(yval)}',
            ha='center',
            va='bottom',
            fontsize=fontsize,
            fontweight=fontweight  # Set the font weight
        )


tad_count = []
tad_sizes = []
size_dist_per_bin_list = []
bin_list = []
min_max_sizes = []
x_ticks = []
x_label = []
with open(f"{BASE_PATH}/tad_info.txt", "w") as outfile:
    txt = f"data\tcount\tmin_size\tmean_size\tmax_size\n"
    outfile.write(txt)
    for org, resol_list, chrom_list in zip(ORGANISM, RESOLS, CHROMS):
        for resol in resol_list:
            count = 0
            tad_size = []
            size_dist_per_bin = []
            bins = []
            min_max_size = []
            for chr in chrom_list:
                domains = f"{BASE_PATH}/{org}/cuda_{org}_{resol}_chr{chr}.bed"
                print(f"Processing {domains}")
                with open(domains, "r") as infile:
                    for line in infile:
                        count = count+1
                        columns = line.strip().split('\t')
                        tad_size.append(
                            int((int(columns[3])-int(columns[1]))/1000))
            tad_count.append(count)
            min_size = min(tad_size)
            mean_size = round(np.mean(tad_size))
            max_size = max(tad_size)
            tad_sizes.append(tad_size)
            min_max_size.append(min_size)
            min_max_size.append(mean_size)
            min_max_size.append(max_size)
            min_max_sizes.append(min_max_size)

            for size in range(min_size*1000, (max_size*1000)+resol, resol):
                size = int(size/1000)
                size_dist_per_bin.append((tad_size.count(size)/count)*100)
                bins.append(size)
            size_dist_per_bin_list.append(size_dist_per_bin)
            bin_list.append(bins)
            tick = org.upper() + " " + str(int(resol/1000)) + "Kb"
            x_ticks.append(tick)
            x_label.append(tick)
            txt = f"{org}_{resol}:\t{count}\t{min_size}\t{mean_size}\t{max_size}\n"
            outfile.write(txt)

colors = sns.color_palette(palette="rocket", n_colors=6, as_cmap=False)
palette = itertools.cycle(colors)
titles = ["Number of TAD", "TAD Size", "Size Distribution (GM12878 5Kb)",
          "Size Distribution (GM12878 10Kb)", "Size Distribution (CH12LX 5Kb)", "Size Distribution (CH12LX 10Kb)"]

plt.rcParams.update({'font.size': 24})
fig, axs = plt.subplots(2, 3, figsize=(30, 20))


# Bar plot
bars = sns.barplot(x=x_label, y=tad_count, palette=colors, ax=axs[0, 0])
add_annotations(axs[0, 0], bars.patches, 24)
axs[0, 0].set_title(titles[0], fontsize=28)
axs[0, 0].set_ylabel("count")
axs[0, 0].tick_params(axis='x', labelsize=18)


# Line plots
for i in range(4):
    row = 1 if i >= 2 else 0
    col = (i + 1) % 3
    axs[row, col].plot(bin_list[i], size_dist_per_bin_list[i],
                       label=x_label[i], color=colors[i])
    axs[row, col].set_title(titles[i+2], fontsize=28)
    axs[row, col].set_ylabel("% (per bin)")
    axs[row, col].set_xlabel("bin (Kb)")

    axs[row, col].axvline(x=min_max_sizes[i][1], color='green', linestyle='--')
    axs[row, col].text(min_max_sizes[i][1]+250, 0.80, f"{min_max_sizes[i][1]}Kb", color='r', ha='right', va='top', rotation=90,
                       transform=axs[row, col].get_xaxis_transform())


# Box plot
axs[1, 2].set_ylabel('size (Kb)')
# vplot = axs[0, 1].violinplot(tad_sizes, showmeans=True, showextrema=True)
# for pc, color in zip(vplot['bodies'], colors):
#     pc.set_facecolor(color)  # Set the face color of the violin
#     pc.set_edgecolor('black')  # Optional: Set the edge color
#     pc.set_alpha(0.7)  # Optional: Set the transparency level

bplot = axs[1, 2].boxplot(tad_sizes, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

axs[1, 2].set_title(titles[1], fontsize=28)
axs[1, 2].set_xticklabels(x_ticks)
axs[1, 2].tick_params(axis='x', labelsize=18)


plt.tight_layout()
plt.savefig("tad_info.png", dpi=300, bbox_inches="tight")
