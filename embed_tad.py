import argparse
import numpy as np
import networkx as nx
from sklearn.cluster import HDBSCAN
import pandas as pd
from itertools import groupby
from karateclub import NetMF
import time
from scipy.ndimage import gaussian_filter
from tad_writers import *
from tad_scores import *
from tad_plots import *
from et_logger import *
import cudf
import cugraph 

SIGMA = 1.0
DIMENSION = 455
ITERATION = 16
ORDER = 2
NEGATIVE_SAMPLE = 1
SEED = 0
METRICS = "euclidean"
MIN_TAD_SIZE = 100000
MAX_TAD_SIZE = 5000000


def clustering(logger, input_file, resolution, output_file):
    logger.info(f"Reading {input_file}")
    print(f"Reading {input_file}")
    X = np.loadtxt(input_file)

    logger.info(f"Applying Gaussian filter...")
    print(f"Applying Gaussian filter...")
    X = gaussian_filter(X, sigma=SIGMA)

    tad_regions = pd.DataFrame()
    tad_regions["start"] = ""
    tad_regions["start (basepairs)"] = ""
    tad_regions["end"] = ""
    tad_regions["end (basepairs)"] = ""
    tad_regions["count"] = ""

    logger.info(f"Creating graph...")
    print(f"Creating graph...")
    x_src, x_dst = np.where(X > 0)
    x_weights = X[x_src, x_dst]
    edges = cudf.DataFrame({
        'src': x_src,
        'dst': x_dst,
        'weights': x_weights
    })

    # Create a Graph from the edges DataFrame
    G = cugraph.Graph()
    G.from_cudf_edgelist(edges, source='src', destination='dst', edge_attr='weights')
    # G = nx.from_numpy_array(X)

    logger.info(f"Running NetMF to embed the input matrix...")
    print(f"Running NetMF to embed the input matrix...")
    now = time.time()
    embeddings_model = NetMF(dimensions=DIMENSION, iteration=ITERATION,
                             order=ORDER, negative_samples=NEGATIVE_SAMPLE, seed=SEED)
    embeddings_model.fit(G)
    embeddings = embeddings_model.get_embedding()
    embedding_time = round(time.time() - now, 2)
    logger.info(f"Total time to embed: {embedding_time} seconds")
    print(f"Total time to embed: {embedding_time} seconds")

    logger.info(f"Running HDBSCAN to cluster...")
    print(f"Running HDBSCAN to cluster...")
    now = time.time()
    clusterer = HDBSCAN(metric=METRICS)
    cluster = clusterer.fit(embeddings)
    clustering_time = round(time.time() - now, 2)
    logger.info(f"Total time to Cluster: {clustering_time} seconds")
    print(f"Total time to Cluster: {clustering_time} seconds")

    logger.info(f"Recording predicted TADs...")
    print(f"Recording predicted TADs...")

    consecutive_counts = [sum(1 for _ in group)
                          for _, group in groupby(cluster.labels_)]
    MIN_BINS = int(round(MIN_TAD_SIZE/resolution, 0))
    MAX_BINS = int(round(MAX_TAD_SIZE/resolution, 0))
    start = 1
    end = 1
    for i in range(0, len(consecutive_counts)):
        end = start + consecutive_counts[i] - 1
        if consecutive_counts[i] >= MIN_BINS and consecutive_counts[i] <= MAX_BINS:
            tad_regions.loc[len(tad_regions.index)] = [
                start, (start-1)*resolution, end, end*resolution, consecutive_counts[i]]
        start = start + consecutive_counts[i]

    out_file = output_file +"_embed_tad"
    write_tads(tads=tad_regions, file=out_file)

    logger.info(f"Plotting heatmap...")
    print(f"Plotting heatmap...")
    draw_heatmap(X, tad_regions, file=out_file)
    draw_heatmap_area(X, tad_regions, file=out_file)

    tads = tad_regions[["start", "end"]]
    tads["start"] -= 1
    tads["end"] -= 1
    tads = tads.to_numpy()
    tq = get_tad_quality(tads, X)
    logger.info(f"Calculated TAD Quality: {tq}")
    print(f"Calculated TAD Quality: {tq}")
    write_tad_quality(tad_quality=tq, file=out_file)


def main():
    parser = argparse.ArgumentParser(
        description="Welcome to EmbedTAD.")
    parser.add_argument("--input", type=str, required=True, help="Input file")
    parser.add_argument("--resolution", type=int,
                        required=True, help="Resolution")
    parser.add_argument("--output", type=str,
                        required=True, help="Output file")

    args = parser.parse_args()

    input_file = args.input
    resol = args.resolution
    output_file = args.output

    parts = input_file.split(r"/|//|\|\\", args.filepath)
    filename = parts[-1].replace(".*", "")

    logger = base_logger(output_file)
    logger.info(f"______Starting Pipeline______")
    now = time.time()
    try:
        clustering(logger=logger, input_file=input_file,
                   resolution=resol, output_file=output_file+filename)
    except Exception as ex:
        logger.error(ex)
    logger.info(f"Total running time: {round(time.time() - now, 2)} seconds")
    logger.info(f"______Finished______")


if __name__ == "__main__":
    main()
