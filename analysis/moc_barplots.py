import seaborn as sns
import matplotlib.pyplot as plt


def add_annotations(ax, bars, fontsize=14):
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        fontweight = 'bold' if i == 0 else 'normal'
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f'{yval:.2f}',
            ha='center',
            va='bottom',
            fontsize=fontsize,
            fontweight=fontweight  # Set the font weight
        )


x = ["EmbedTAD",	"IC-Finder",	"ClusterTAD",	"CASPIAN",
     "TopDom",	"Armatus",	"HiCseg",	"Spectral"]
y1 = [93.0452,	73.6848,	56.9164,	76.7552,	89.8796,	89.2964,	73.528,	70.7148]
y2 = [94.128,	62.53,	62.946,	89.754,	93.724,	91.286,	53.288,	72.216]
y3 = [93.544,	75.494,	59.604,	83.43,	91.268,	90.116,	67.028,	72.406]
y4 = [93.656,	76.85,	57.268,	79.598,	88.77,	89.188,	75.906,	70.808]
y5 = [91.998,	76.476,	52.932,	70.75,	87.992,	89.112,	83.84,	69.538]
y6 = [91.9,	    77.074,	51.832,	60.244,	87.644,	86.78,	87.578,	68.606]

colors = sns.color_palette("Paired", 8)
labels = ["EmbedTAD",	"IC-Finder",	"ClusterTAD",
          "CASPIAN", "TopDom",	"Armatus",	"HiCseg",	"Spectral"]
titles = ["Overall", "4 noise level", "8 noise level",
          "12 noise level", "16 noise level", "20 noise level"]

plt.rcParams.update({'font.size': 22})
fig, axes = plt.subplots(2, 3, figsize=(30, 20))
for ax, y_data, title in zip(axes.flat, [y1, y2, y3, y4, y5, y6], titles):
    bars = sns.barplot(x=x, y=y_data, palette=colors, ax=ax)
    add_annotations(ax, bars.patches, 22)
    ax.get_xaxis().set_visible(False)
    ax.set_title(title, fontsize=28)

handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
fig.legend(handles, labels, loc='upper center', ncol=8,
           fontsize=26, bbox_to_anchor=(0.5, 1.1))


plt.tight_layout(rect=[0, 0, 1, 1.05])
plt.savefig("moc_barplots.png", dpi=300, bbox_inches="tight")
