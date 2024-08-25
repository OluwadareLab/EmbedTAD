import csv
import hicstraw
import numpy as np
from typing import List
import logging
import time
import math


def bed2mat(bed, chr_size, res=10000):
    N = math.ceil(chr_size/res)
    mat = np.zeros((N, N))
    for i in range(0, len(bed), 1):
        mat[int(bed[i].binX / res), int(bed[i].binY / res)] = bed[i].counts
        mat[int(bed[i].binY / res), int(bed[i].binX / res)] = bed[i].counts

    return mat


def to_square_matrix(chrom_size_file: str, in_file: str, out_path: str, out_prefix: str, chroms: List[str], resols: List[int] = [5000], d_type: str = "observed", norm: str = "NONE", logger=None):
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
            output_file = out_path + out_prefix + \
                str(res) + "_" + "chr"+str(chr) + ".mat"
            print(f"converting to: {output_file}")
            logger.info(f"converting to: {output_file}")
            bed = hicstraw.straw(d_type, norm,
                                 in_file, chr, chr, 'BP', res)
            mat = bed2mat(bed, chrom_size["chr"+chr], res)
            print(f"saving: {output_file}")
            logger.info(f"saving: {output_file}")
            np.savetxt(output_file, mat, delimiter=" ", fmt="%.2f")
            print(f"File saved to: {output_file}")
            logger.info(f"File saved to: {output_file}")
            total_running_time = round(time.time() - start_time, 2)
            print(f"Total time (seconds) taken: {total_running_time}")
            logger.info(f"Total time (seconds) taken: {total_running_time}")
