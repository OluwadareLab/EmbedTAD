from heatmap import *
from tad_scores import *
import pandas as pd

BASE_PATH = "/home/mohit/Documents/project/embed_tad"
FILENAME_PREFIX = ["ch12lx", "gm12878"]
CHROMS = [[2, 18], [3, 19]]
RESOLS = [[10000, 5000], [10000, 5000]]
REGION_START = [[40000000, 40000000], [40000000, 40000000]]
REGION_END = [[44000000, 44000000], [44000000, 44000000]]

if __name__ == "__main__":
    for chroms, resls, prefix, starts, ends, in zip(CHROMS, RESOLS, FILENAME_PREFIX, REGION_START, REGION_END):
        for res in resls:
            for chr, start, end in zip(chroms, starts, ends):
                matrix = f"{BASE_PATH}/data/raw/{prefix}/{prefix}_{res}_chr{chr}.txt"
                print(f'Processing matrix -> {matrix}')
                tads = f"{BASE_PATH}/data/results/gpu/{prefix}/{prefix}_{res}_chr{chr}.txt"
                print(f'Processing bed -> {matrix}')
                output = f"{BASE_PATH}/plots/tad_{prefix}_{res}_chr{chr}.png"
                vis = Triangle(matrix, res, chr, start, end)
                vis.matrix_plot()
                vis.plot_TAD(tads, res, linewidth=3)
                print(f'Writing -> {output}')
                vis.outfig(output)