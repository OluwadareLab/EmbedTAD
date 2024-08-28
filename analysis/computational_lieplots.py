import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


titles = ["MoC", "TAD Quality", "Graph Creation Time", "Embedding Time"]
y_labels = ["MoC", "TAD Quality", "seconds", "seconds"]
moc = {"nl": ["4", "8", "12", "16", "20", "4", "8", "12", "16", "20"],
       "values": [94.39, 92.81, 92.87, 91.55, 93.03, 94.77, 93.31, 93.05, 91.39, 92.65],
       "machine": ["cpu", "cpu", "cpu", "cpu", "cpu", "gpu", "gpu", "gpu", "gpu", "gpu"]
       }
moc = pd.DataFrame(moc)
tq = {"nl": ["4", "8", "12", "16", "20", "4", "8", "12", "16", "20"],
      "values": [8.06, 9.37, 9.82, 10.74, 8.1, 9.46, 9.84, 10.81, 10.93, 10.94],
      "machine": ["cpu", "cpu", "cpu", "cpu", "cpu", "gpu", "gpu", "gpu", "gpu", "gpu"]
      }
tq = pd.DataFrame(tq)
graph_time = {"nl": ["4", "8", "12", "16", "20", "4", "8", "12", "16", "20"],
              "values": [18.43, 18.17, 21.31, 21.06, 23.67, 0.96, 0.6, 0.74, 0.7, 0.75],
              "machine": ["cpu", "cpu", "cpu", "cpu", "cpu", "gpu", "gpu", "gpu", "gpu", "gpu"]
              }
graph_time = pd.DataFrame(graph_time)
embed_time = {"nl": ["4", "8", "12", "16", "20", "4", "8", "12", "16", "20"],
              "values": [228.48, 209.44, 262.91, 263.17, 303.22, 138.56, 112.89, 130.43, 130.19, 141.6],
              "machine": ["cpu", "cpu", "cpu", "cpu", "cpu", "gpu", "gpu", "gpu", "gpu", "gpu"]
              }
embed_time = pd.DataFrame(embed_time)


# fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# values = [moc, tq, graph_time, embed_time]
# palette = iter(sns.color_palette("Set1", len(values)))

# # Loop through each subplot and plot the data
# for i, ax in enumerate(axes.flat):
#     sns.lineplot(data=values[i], x="nl", y="values", hue="machine", marker='o',
#                  palette=sns.color_palette("Set1"), ax=ax)
#     ax.set_title(titles[i], fontsize=18)  # Set the title of each subplot
#     ax.set_ylabel(y_labels[i], fontsize=14)  # Set the y-axis label with increased font size
#     ax.set_xlabel('nl', fontsize=14)  # Set the x-axis label
#     ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))  # Format y-axis to 2 decimal points

# # Adjust the legend to be outside the plot
# handles, labels = ax.get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper center', ncol=4, fontsize=12, bbox_to_anchor=(0.5, 1.05))

# # Adjust layout to prevent overlap and make the figure more readable
# plt.tight_layout(rect=[0, 0, 1, 0.95])

# # Show the figure
# plt.show()
plt.rcParams.update({'font.size': 22})
fig, axes = plt.subplots(2, 2, figsize=(30, 20))
for ax, data, title, ylabel in zip(axes.flat, [moc, tq, graph_time, embed_time], titles, y_labels):
    # data = data.pivot(index="machine", columns="nl", values="values")
    bars = sns.lineplot(data=data.dropna(), x="nl", palette=sns.color_palette("Set2"),
                        y="values", hue="machine", style="machine", markers=["X", "o"], markersize=14, estimator=None,
                        linewidth=4,  ax=ax)
    ax.set_title(title, fontsize=28)
    ax.set_xlabel("Noise Level")
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

plt.savefig("computational_lineplots.png", dpi=300, bbox_inches="tight")
