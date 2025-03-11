import time
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
import networkx as nx
from netmf import NetMF
from sklearn.cluster import HDBSCAN
from itertools import groupby
from analysis.tad_scores import *
from tad_writers import *
from tad_plots import *
from assembler import assembler
import warnings
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
warnings.simplefilter(action='ignore')


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
OVERLAP_THRESHOLD = 30_00_000
DRAW_TADS_COUNTS = 5


def clustering(logger, input_file, resol, output_file, norm: bool = True):
    clustering_start_time = time.time()

    MIN_BINS = int(math.ceil(MIN_TAD_SIZE/resol))
    MAX_BINS = int(math.ceil(MAX_TAD_SIZE/resol))

    tads = pd.DataFrame()
    tads["start"] = ""
    # tads["start (basepairs)"] = ""
    tads["end"] = ""
    # tads["end (basepairs)"] = ""
    # tads["count"] = ""

    logger.info(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:  Reading {input_file}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:  Reading {input_file}")
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

    prev_tads = pd.DataFrame()
    prev_tads["start"] = ""
    prev_tads["end"] = ""
    cur_tads = pd.DataFrame()
    cur_tads["start"] = ""
    cur_tads["end"] = ""
    silhouette = 0
    db_index = 0
    ch_index = 0
    total = 0

    for start_row in range(0, n_rows, batch_size):
        total += 1
        end_row = min(start_row + batch_size, n_rows)
        boundary_threshold = int(OVERLAP_THRESHOLD/resol)
        e_position = end_row
        s_position = e_position - boundary_threshold
        if start_row > 0:
            e_position = start_row
            start_row = start_row - boundary_threshold
            s_position = start_row
        logger.info(f"Processing {start_row}-{end_row} data")
        print(f"Processing {start_row}-{end_row} data")

        chunk = raw_matrix[start_row:end_row, start_row:end_row]
        if norm:
            logger.info(f"Applying Gaussian filter")
            print(f"Applying Gaussian filter")
            chunk = gaussian_filter(chunk, sigma=SIGMA)

        logger.info(f"Creating graph")
        print(f"Creating graph")
        graph_start_time = time.time()
        G = nx.from_numpy_array(chunk)
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

        silhouette += silhouette_score(chunk, clusters.labels_)
        db_index += davies_bouldin_score(chunk, clusters.labels_)
        ch_index += calinski_harabasz_score(chunk, clusters.labels_)

        c_counts = [sum(1 for _ in group)
                    for _, group in groupby(clusters.labels_)]

        start = start_row
        end = 1
        print(f"Start: {s_position}, End: {e_position}")
        for i in range(0, len(c_counts)):
            end = start + c_counts[i] - 1
            if c_counts[i] >= MIN_BINS and c_counts[i] <= MAX_BINS:
                if (start >= s_position and start <= e_position) or (end >= s_position and end <= e_position):
                    cur_tads.loc[len(cur_tads.index)] = [start, end]
                else:
                    tads.loc[len(tads.index)] = [start, end]
            start = start + c_counts[i]

        for i in range(len(tads) - 1):
            if (int(tads.loc[i, 'start']) >= int(s_position) and int(tads.loc[i, 'start']) <= int(e_position)) or (int(tads.loc[i, 'end']) >= int(s_position) and int(tads.loc[i, 'end']) <= int(e_position)):
                prev_tads.loc[len(prev_tads.index)] = [
                    int(tads.loc[i, 'start']), int(tads.loc[i, 'end'])]

        prev_tq = get_tad_quality(prev_tads.to_numpy(), raw_matrix)
        cur_tq = get_tad_quality(cur_tads.to_numpy(), raw_matrix)

        if len(prev_tads):
            cond = tads.apply(tuple, axis=1).isin(
                prev_tads.apply(tuple, axis=1))
            tads.drop(tads[cond].index, inplace=True)
            tads.reset_index(drop=True, inplace=True)
        if cur_tq >= prev_tq:
            tads = pd.concat([tads, cur_tads], ignore_index=True)
        else:
            tads = pd.concat([tads, prev_tads], ignore_index=True)

        prev_tads = prev_tads.drop(prev_tads.index).reset_index(drop=True)
        cur_tads = cur_tads.drop(cur_tads.index).reset_index(drop=True)
        tads.reset_index(drop=True, inplace=True)

    tads = tads.sort_values(by=['start', 'end'])

    logger.info(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")
    print(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")

    silhouette /= total
    db_index /= total
    ch_index /= total
    tad_quality = get_tad_quality(tads.to_numpy(), raw_matrix)

    quality_file = output_file+"_quality_score.txt"
    logger.info(f"Writing TAD Quality: {tad_quality} to {quality_file}")
    print(f"Writing TAD Quality: {tad_quality} to {quality_file}")
    quality_score = f"TAD Quality: {tad_quality}\nSilhouette Score: {silhouette}\nDavies Bouldin Index: {db_index}\nCalinski Harabasz Index: {ch_index}"
    write_quality_score(quality_text=quality_score, file=quality_file)

    logger.info(f"Writing {tads.shape} TAD regions")
    print(f"Writing {tads.shape} TAD regions")
    tads[['start', 'end']] *= resol
    tads.to_csv(output_file + ".txt", sep="\t", header=False, index=False)

    # logger.info(f"Plotting heatmap of first {DRAW_TADS_COUNTS} TADs")
    # print(f"Plotting heatmap of first {DRAW_TADS_COUNTS} TADs")
    # draw_heatmap_area(raw_matrix, tads, file=output_file,
    #                   first_tad_count=DRAW_TADS_COUNTS)

    logger.info(
        f"Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")
    print(
        f"Total clustering time: {round(time.time()-clustering_start_time, 2)} seconds")
