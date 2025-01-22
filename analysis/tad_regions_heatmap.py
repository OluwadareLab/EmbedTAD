from heatmap import *
from tad_scores import *
import pandas as pd

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"
FILENAME_PREFIX = ["ch12lx", "gm12878_combined"]
CHROMS = [[2, 18], [3, 19]]
RESOLS = [[10000, 5000], [10000, 5000]]
REGION_START = [[79000000, 50000000], [80500000, 40500000]]
REGION_END = [[84500000, 55000000], [84500000, 44000000]]

# FILENAME_PREFIX = ["ch12lx", "gm12878_combined"]
# CHROMS = [[2, 18], [3, 19]]
# RESOLS = [[5000], [5000]]
# REGION_START = [[50000000], [40500000]]
# REGION_END = [[55000000], [44000000]]

if __name__ == "__main__":
    for chroms, resls, prefix, starts, ends, in zip(CHROMS, RESOLS, FILENAME_PREFIX, REGION_START, REGION_END):
        for res in resls:
            for chr, start, end in zip(chroms, starts, ends):
                matrix = f"{BASE_PATH}/matrix/{prefix}_{res}_chr{chr}.txt"
                print(f'Processing matrix -> {matrix}')
                pre=prefix.replace("_combined", "")
                tads = f"{BASE_PATH}/chip_sig/{pre}/cuda_{pre}_{res}_chr{chr}.bed"
                print(f'Processing bed -> {matrix}')
                output = f"{BASE_PATH}/tadtool/{prefix}_{res}_chr{chr}.png"
                vis = Triangle(matrix, res, chr, start, end)
                vis.matrix_plot()
                vis.plot_TAD(tads, linewidth=2)
                print(f'Writing -> {output}')
                vis.outfig(output)
