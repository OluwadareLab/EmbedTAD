import time
import pandas as pd
import numpy as np
import cupy
from cupyx.scipy.ndimage import gaussian_filter
import cugraph
from cuda_netmf import NetMF
from sklearn.cluster import HDBSCAN
from itertools import groupby
from tad_scores import *
from tad_writers import *
from tad_plots import *


BATCH_SIZE_THRESHOLD = 5000
SIGMA = 1.0
DIMENSION = 455
ITERATION = 16
ORDER = 2
NEGATIVE_SAMPLE = 1
SEED = 0
METRIC = "euclidean"
MIN_TAD_SIZE = 100000
MAX_TAD_SIZE = 5000000
DRAW_TADS_COUNTS = 5


def clustering(logger, input_file, resol, output_file, norm: bool = False):
    clustering_start_time = time.time()

    MIN_BINS = int(math.ceil(MIN_TAD_SIZE/resol))
    MAX_BINS = int(math.ceil(MAX_TAD_SIZE/resol))

    tad_regions = pd.DataFrame()
    tad_regions["start"] = ""
    tad_regions["start (basepairs)"] = ""
    tad_regions["end"] = ""
    tad_regions["end (basepairs)"] = ""
    tad_regions["count"] = ""

    logger.info(f"Reading {input_file}")
    print(f"Reading {input_file}")
    raw_matrix = np.loadtxt(input_file)
    n_rows, n_cols = raw_matrix.shape
    if n_rows != n_cols:
        logger.info(f"Matrix is not square")
        print(f"Matrix is not square")
        return

    batch_size = n_rows if n_rows < BATCH_SIZE_THRESHOLD else int(
        math.ceil(n_rows/math.ceil(n_rows/BATCH_SIZE_THRESHOLD)))
    logger.info(f"Batch size: {batch_size}")
    print(f"Batch size: {batch_size}")

    for start_row in range(0, n_rows, batch_size):
        end_row = min(start_row + batch_size, n_rows)
        logger.info(f"Processing {start_row}-{end_row} data")
        print(f"Processing {start_row}-{end_row} data")

        chunk = raw_matrix[start_row:end_row, start_row:end_row]
        if norm:
            logger.info(f"Applying Gaussian filter")
            print(f"Applying Gaussian filter")
            chunk = cupy.asarray(chunk)
            chunk = gaussian_filter(chunk, sigma=SIGMA)
            chunk = cupy.asnumpy(chunk)

        logger.info(f"Creating graph")
        print(f"Creating graph")
        graph_start_time = time.time()
        G = cugraph.from_numpy_array(chunk)
        logger.info(
            f"Graph creation time: {round(time.time()-graph_start_time, 2)} seconds")
        print(
            f"Graph creation time: {round(time.time()-graph_start_time, 2)} seconds")

        logger.info(f"Creating embedded data representation")
        print(f"Creating embedded data representation")
        embedding_start_time = time.time()
        embeddings_model = NetMF(dimensions=DIMENSION, iteration=ITERATION,
                                 order=ORDER, negative_samples=NEGATIVE_SAMPLE, seed=SEED)
        embeddings_model.fit(G)
        embeddings = embeddings_model.get_embedding()
        logger.info(
            f"Embedding creation time: {round(time.time()-embedding_start_time, 2)} seconds")
        print(
            f"Embedding creation time: {round(time.time()-embedding_start_time, 2)} seconds")

        logger.info(f"Running cluster algorithm")
        print(f"Running cluster algorithm")
        cluster_algo_start_time = time.time()
        clusterer = HDBSCAN(metric=METRIC)
        clusters = clusterer.fit(embeddings)
        logger.info(
            f"Clustering algorithm taken time: {round(time.time()-cluster_algo_start_time, 2)} seconds")
        print(
            f"Clustering algorithm taken time: {round(time.time()-cluster_algo_start_time, 2)} seconds")

        print("Recording TAD regions")
        logger.info("Recording TAD regions")
        c_counts = [sum(1 for _ in group)
                    for _, group in groupby(clusters.labels_)]

        start = 1+start_row
        end = 1
        for i in range(0, len(c_counts)):
            end = start + c_counts[i] - 1
            if c_counts[i] >= MIN_BINS and c_counts[i] <= MAX_BINS:
                tad_regions.loc[len(tad_regions.index)] = [
                    start, (start-1)*resol, end, end*resol, c_counts[i]]
            start = start + c_counts[i]

    logger.info(f"Writing {tad_regions.shape} TAD regions")
    print(f"Writing {tad_regions.shape} TAD regions")
    tad_regions.to_csv(output_file + ".bed", sep="\t",
                       header=False, index=False)

    tads = tad_regions[["start", "end"]]
    tads["start"] -= 1
    tads["end"] -= 1
    tads = tads.to_numpy()
    tad_quality = get_tad_quality(tads, raw_matrix)
    tad_quality_file = output_file+"_tq.txt"
    logger.info(f"Writing TAD Quality: {tad_quality} to {tad_quality_file}")
    print(f"Writing TAD Quality: {tad_quality} to {tad_quality_file}")
    write_tad_quality(tad_quality=tad_quality, file=tad_quality_file)

    logger.info(f"Plotting heatmap of first {DRAW_TADS_COUNTS} TADs")
    print(f"Plotting heatmap of first {DRAW_TADS_COUNTS} TADs")
    draw_heatmap_area(raw_matrix, tad_regions, file=output_file,
                      first_tad_count=DRAW_TADS_COUNTS)

    logger.info(
        f"Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")
    print(
        f"Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")
