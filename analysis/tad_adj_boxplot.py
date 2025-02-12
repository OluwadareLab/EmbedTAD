import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

plt.rcParams.update({'font.size': 14})

df = pd.read_csv(f"/home/mohit/Documents/project/embed_tad/data/results/tad_callers/gm12878_rsqr.csv")

# df = df[df["Resolution"] == "5Kb"]
reshaped_df = df.melt(id_vars=["Resolution"], var_name="Algorithm", value_name="Value")

summary = reshaped_df.groupby(['Resolution', 'Algorithm'])['Value'].agg(['min', 'median', 'max']).reset_index()
# Rename the columns for better clarity
summary.columns = ['Resolution', 'Algorithm', 'Min Value', 'Median Value', 'Max Value']
# Save the summary to a CSV file
summary.to_csv('/home/mohit/Documents/project/embed_tad/plots/gm12878_rsqr_statistics.csv', index=False)

# plt.figure(figsize=(12, 5))
# sns.boxplot(data=reshaped_df, x="Algorithm", y="Value", hue="Resolution", fill=False, gap=.1)
# plt.title("GM12878")
# plt.xlabel(f"Algorithm")
# plt.ylabel(f"TADadjR$^2$")
# plt.savefig("gm12878_adj_square_boxplot.png", dpi=600, bbox_inches="tight")

# Interpolation to create 150 points per algorithm-resolution pair
smooth_data = []
for algo in reshaped_df['Algorithm'].unique():
    algo_data = reshaped_df[reshaped_df['Algorithm'] == algo]
    for resolution in algo_data['Resolution'].unique():
        sub_data = algo_data[algo_data['Resolution'] == resolution]
        x_original = np.arange(len(sub_data))
        x_smooth = np.linspace(x_original.min(), x_original.max(), 150)
        y_smooth = make_interp_spline(x_original, sub_data['Value'])(x_smooth)
        
        smooth_data.append(pd.DataFrame({
            "Algorithm": [algo] * len(x_smooth),
            "Value": y_smooth,
            "Resolution": [resolution] * len(x_smooth),
            "X_Axis": x_smooth  # Create a shared x-axis for interpolation
        }))

# Combine smooth data
smooth_df = pd.concat(smooth_data, ignore_index=True)
for resolution in smooth_df["Resolution"].unique():
    # Filter data for the current resolution
    res_data = smooth_df[smooth_df["Resolution"] == resolution]
    
    # Create a 2x4 grid of line plots for each algorithm
    g = sns.FacetGrid(res_data, col="Algorithm", col_wrap=4, height=4, hue="Algorithm", sharey=False, sharex=False)
    g.map_dataframe(sns.lineplot, x="X_Axis", y="Value", linewidth=3)
    
    # Add labels, titles, and adjust layout
    g.set_axis_labels("Distance (Kb)", f"TADadjR$^2$")
    g.set_titles("{col_name}")
    g.tight_layout(pad=3.0)  # Add padding to reduce overlap
    g.fig.subplots_adjust(top=0.9)  # Further adjust the top margin
    # g.fig.suptitle(f"GM12878 chr19 at {resolution} ", fontsize=16)
    plt.savefig(f"/home/mohit/Documents/project/embed_tad/plots/gm12878_{resolution}_rsqr_lineplots.png", dpi=600, bbox_inches="tight")


df = pd.read_csv(f"/home/mohit/Documents/project/embed_tad/data/results/tad_callers/ch12lx_rsqr.csv")
# df = df[df["Resolution"] == "5Kb"]
reshaped_df = df.melt(id_vars=["Resolution"], var_name="Algorithm", value_name="Value")
summary = reshaped_df.groupby(['Resolution', 'Algorithm'])['Value'].agg(['min', 'median', 'max']).reset_index()
# Rename the columns for better clarity
summary.columns = ['Resolution', 'Algorithm', 'Min Value', 'Median Value', 'Max Value']
# Save the summary to a CSV file
summary.to_csv('/home/mohit/Documents/project/embed_tad/plots/ch12lx_rsqr_statistics.csv', index=False)

# plt.figure(figsize=(12, 5))
# sns.boxplot(data=reshaped_df, x="Algorithm", y="Value", hue="Resolution", fill=False, gap=.1)
# plt.title("CH12LX")
# plt.xlabel(f"Algorithm")
# plt.ylabel(f"TADadjR$^2$")
# plt.savefig("ch12lx_adj_square_boxplot.png", dpi=600, bbox_inches="tight")

smooth_data = []
for algo in reshaped_df['Algorithm'].unique():
    algo_data = reshaped_df[reshaped_df['Algorithm'] == algo]
    for resolution in algo_data['Resolution'].unique():
        sub_data = algo_data[algo_data['Resolution'] == resolution]
        x_original = np.arange(len(sub_data))
        x_smooth = np.linspace(x_original.min(), x_original.max(), 150)
        y_smooth = make_interp_spline(x_original, sub_data['Value'])(x_smooth)
        
        smooth_data.append(pd.DataFrame({
            "Algorithm": [algo] * len(x_smooth),
            "Value": y_smooth,
            "Resolution": [resolution] * len(x_smooth),
            "X_Axis": x_smooth  # Create a shared x-axis for interpolation
        }))

# Combine smooth data
smooth_df = pd.concat(smooth_data, ignore_index=True)
for resolution in smooth_df["Resolution"].unique():
    # Filter data for the current resolution
    res_data = smooth_df[smooth_df["Resolution"] == resolution]
    
    # Create a 2x4 grid of line plots for each algorithm
    g = sns.FacetGrid(res_data, col="Algorithm", col_wrap=4, height=4, hue="Algorithm", sharey=False, sharex=False)
    g.map_dataframe(sns.lineplot, x="X_Axis", y="Value", linewidth=3)
    
    # Set consistent x and y axis limits
    x_min, x_max = 0, 150  # Example: Adjust as needed
    y_min, y_max = 0, 1    # Example: Adjust as needed

    for ax in g.axes.flat:
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    
    # Add labels, titles, and adjust layout
    g.set_axis_labels("Distance (Kb)", f"TADadjR$^2$")
    g.set_titles("{col_name}")
    g.tight_layout(pad=3.0)  # Add padding to reduce overlap
    g.fig.subplots_adjust(top=0.9)  # Further adjust the top margin
    # g.fig.suptitle(f"CH12LX chr18 at {resolution} ", fontsize=16)
    plt.savefig(f"/home/mohit/Documents/project/embed_tad/plots/ch12lx_{resolution}_rsqr_lineplots.png", dpi=600, bbox_inches="tight")