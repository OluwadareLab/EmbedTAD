import numpy as np
import cooler

def matrix_to_cool(martix_uri, binsize, chrom, cool_uri):
    matrix = np.loadtxt(martix_uri)
    chromsizes = cooler.util.fetch_chromsizes('hg19').loc[chrom:chrom]
    bins = cooler.binnify(chromsizes, binsize)
    pixels = cooler.create.ArrayLoader(bins, matrix, chunksize=100000)
    cooler.create_cooler(cool_uri, bins, pixels, assembly='hg19')