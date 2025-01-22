import csv
import hicstraw
import numpy as np
from typing import List
import logging
import time
import math
import pandas as pd
import cooler
import warnings
warnings.simplefilter(action='ignore')


def cool_to_matrix(filepath, filename, chr):
    c = cooler.Cooler(f"{filepath}/{filename}")
    chromosome = f"chr{chr}"
    chr_matrix = c.matrix(balance=False).fetch(chromosome)
    print(
        f"Shape of the chromosome {chromosome} square matrix: {chr_matrix.shape}")
    output_filename = filename.replace(".cool", "")
    np.savetxt(
        X=chr_matrix, fname=f"{filepath}/{output_filename}_{chromosome}.txt", delimiter=" ")


def bed2mat(bed, chr_size, res=10000):
    N = math.ceil(chr_size/res)
    mat = np.zeros((N, N))
    for i in range(0, len(bed), 1):
        mat[int(bed[i].binX / res), int(bed[i].binY / res)] = bed[i].counts
        mat[int(bed[i].binY / res), int(bed[i].binX / res)] = bed[i].counts

    return mat


def to_square_matrix(chrom_size_file: str, in_file: str, out_path: str, out_prefix: str, assembly: str, chroms: List[str], resols: List[int] = [5000], d_type: str = "observed", norm: str = "NONE", logger=None):
    if logger is None:
        logger = logging
    print(f"input file {in_file}")
    logger.info(f"input file {in_file}")
    chrom_size = {}
    with open(chrom_size_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            chrom_size[row[0]] = int(row[1])

    for res in resols:
        for chr in chroms:

            start_time = time.time()
            output_file = out_path + out_prefix
            if norm == "NONE":
                output_file = output_file + "_" + \
                    str(res) + "_" + "chr"+str(chr)
            else:
                output_file = output_file + "_" + norm.lower() + "_" + \
                    str(res) + "_" + "chr"+str(chr)

            print(f"converting to: {output_file}")
            logger.info(f"converting to: {output_file}")
            hic = hicstraw.HiCFile(in_file)
            print(hic.getChromosomes())
            print(hic.getGenomeID())
            print(hic.getResolutions())
            temp = str(chr)
            if assembly.startswith("mm"):
                chr = "chr"+temp
            bed = hicstraw.straw(d_type, norm, in_file,
                                 chr, chr, 'BP', res)
            if assembly.startswith("hg"):
                chr = "chr"+temp
            mat = bed2mat(bed, chrom_size[chr], res)
            print(f"saving: {output_file}")
            logger.info(f"saving: {output_file}")
            # np.savetxt(output_file, mat, delimiter="\t", fmt="%.4f")
            np.save(output_file, mat)
            region(output_file, mat.shape[0], "chr"+str(temp), res)
            print(f"File saved to: {output_file}")
            logger.info(f"File saved to: {output_file}")
            total_running_time = round(time.time() - start_time, 2)
            print(f"Total time (seconds) taken: {total_running_time}")
            logger.info(f"Total time (seconds) taken: {total_running_time}")


def region(file, bins, chr, resol=10000):
    print(f"Bin Size: {bins}")
    start = 0
    end = start+resol
    with open(f"{file}_region.bed", "w") as outfile:
        for bin in range(0, bins):
            columns = [chr, str(start), str(end)]
            line = '\t'.join(columns) + '\n'
            outfile.write(line)
            start = end
            end = start+resol
