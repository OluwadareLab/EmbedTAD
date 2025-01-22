import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

df = pd.read_csv(f"/home/mohit/Documents/project/EmbedTAD/analysis/memory_running_time.csv")
for metric in df['Metric'].unique():
    metric_df = df[df['Metric'] == metric]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax = sns.boxplot(data=metric_df, x="Algorithm", y="Value", fill=False, gap=.2, color="blue")
    # medians = metric_df.groupby(['Algorithm'])['Value'].mean().values
    # nobs = [str(x) for x in medians.tolist()]
    # nobs = [i for i in nobs]

    # pos = range(len(nobs))
    # for tick,label in zip(pos,ax.get_xticklabels()):
    #     ax.text(pos[tick],
    #             medians[tick] + 0.03,
    #             nobs[tick],
    #             horizontalalignment='center',
    #             size='small',
    #             color='b',
    #             weight='semibold')
    if metric=="Time":
        plt.title("Running Time")
        plt.xlabel(f"Algorithm")
        plt.ylabel(f"Seconds")
    if metric=="Memory":
        plt.title("Memory")
        plt.xlabel(f"Algorithm")
        plt.ylabel(f"Mb")
    plt.savefig(f"{metric.lower()}_boxplot.png", dpi=300, bbox_inches="tight")