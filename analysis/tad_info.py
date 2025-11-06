import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.ticker as ticker


# nature_colors = [
#     "#000000", "#e69f00", "#56b3e9", "#009e74", "#f0e442", "#d55e00", "#cc79a7", "#0072b2"
# ]

nature_colors = ["#009e74",  "#0072b2",  "#f0e442", "#d55e00",
                 "#56b3e9", "#e69f00",  "#cc79a7", "#000000"
                 ]

BASE_PATH = "/home/hc0783.unt.ad.unt.edu/mohit/Documents/project/embed_tad/data/embedtad_results/gpu"
ORGANISM = ["gm12878", "ch12lx"]
RESOLS = [[5000, 10000], [5000, 10000]]
CHROMS = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
          [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

OUTPUT_PATH = "/home/hc0783.unt.ad.unt.edu/workspace/codebase/EmbedTAD/analysis"


def add_annotations(ax, bars, fontsize=10):
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
                domains = f"{BASE_PATH}/{org}/{org}_{resol}_chr{chr}.txt"
                print(f"Processing {domains}")
                with open(domains, "r") as infile:
                    for line in infile:
                        count = count+1
                        columns = line.strip().split('\t')
                        tad_size.append(
                            int((int(columns[1])*resol-int(columns[0])*resol)/1000))
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
palette = itertools.cycle(nature_colors)
titles = ["Number of TAD", "TAD Size", "Size Distribution (GM12878 5Kb)",
          "Size Distribution (GM12878 10Kb)", "Size Distribution (CH12LX 5Kb)", "Size Distribution (CH12LX 10Kb)"]

plt.rcParams.update({'font.size': 10})
fig, axs = plt.subplots(2, 3, figsize=(16, 8.5))


# Bar plot
bars = sns.barplot(x=x_label, y=tad_count, palette=nature_colors, ax=axs[0, 0])
add_annotations(axs[0, 0], bars.patches)
axs[0, 0].set_title(titles[0])
axs[0, 0].set_ylabel("count")
axs[0, 0].tick_params(axis='x', labelsize=8)


# Line plots
for i in range(4):
    row = 1 if i >= 2 else 0
    col = (i + 1) % 3
    axs[row, col].plot(bin_list[i], size_dist_per_bin_list[i],
                       label=x_label[i], color=nature_colors[i], linewidth=1)
    axs[row, col].set_title(titles[i+2])
    axs[row, col].set_ylabel("% (per bin)")
    axs[row, col].set_xlabel("bin")

    axs[row, col].axvline(x=min_max_sizes[i][1],
                          color='#0072b2', linestyle='--', linewidth=2)
    axs[row, col].text(min_max_sizes[i][1]+250, 0.55, f"{min_max_sizes[i][1]}Kb", color='#d55e00', ha='right', va='top', rotation=90,
                       transform=axs[row, col].get_xaxis_transform())


# Box plot
axs[1, 2].set_ylabel('Size (Kb)')
# vplot = axs[0, 1].violinplot(tad_sizes, showmeans=True, showextrema=True)
# for pc, color in zip(vplot['bodies'], colors):
#     pc.set_facecolor(color)  # Set the face color of the violin
#     pc.set_edgecolor('black')  # Optional: Set the edge color
#     pc.set_alpha(0.7)  # Optional: Set the transparency level

bplot = axs[1, 2].boxplot(tad_sizes, patch_artist=True)
for patch, color in zip(bplot['boxes'], nature_colors):
    patch.set_facecolor(color)

axs[1, 2].set_title(titles[1])
axs[1, 2].set_xticklabels(x_ticks)
axs[1, 2].tick_params(axis='x', labelsize=8)


plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/tad_info.png", dpi=300, bbox_inches="tight")
