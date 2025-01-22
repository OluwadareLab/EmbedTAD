import csv
# import hicstraw
import numpy as np
from typing import List
import logging
import time
import math
import pandas as pd
import cooler


def cool_to_matrix(filepath, filename, chr):
    c = cooler.Cooler(f"{filepath}/{filename}")
    chromosome = f"chr{chr}"
    chr_matrix = c.matrix(balance=False).fetch(chromosome)
    print(
        f"Shape of the chromosome {chromosome} square matrix: {chr_matrix.shape}")
    output_filename = filename.replace(".cool", "")
    np.savetxt(
        X=chr_matrix, fname=f"{filepath}/{output_filename}_{chromosome}.txt", delimiter=" ")


# def bed2mat(bed, chr_size, res=10000):
#     N = math.ceil(chr_size/res)
#     mat = np.zeros((N, N))
#     for i in range(0, len(bed), 1):
#         mat[int(bed[i].binX / res), int(bed[i].binY / res)] = bed[i].counts
#         mat[int(bed[i].binY / res), int(bed[i].binX / res)] = bed[i].counts

#     return mat


# def to_square_matrix(chrom_size_file: str, in_file: str, out_path: str, out_prefix: str, chroms: List[str], resols: List[int] = [5000], d_type: str = "observed", norm: str = "NONE", logger=None):
#     if logger is None:
#         logger = logging
#     print(f"input file {in_file}")
#     logger.info(f"input file {in_file}")
#     chrom_size = {}
#     with open(chrom_size_file) as f:
#         reader = csv.reader(f, delimiter="\t")
#         for row in reader:
#             chrom_size[row[0]] = int(row[1])

#     for res in resols:
#         for chr in chroms:

#             start_time = time.time()
#             output_file = out_path + out_prefix
#             if norm == "NONE":
#                 output_file = output_file + "_" + \
#                     str(res) + "_" + "chr"+str(chr)
#             else:
#                 output_file = output_file + "_" + norm.lower() + "_" + \
#                     str(res) + "_" + "chr"+str(chr)

#             print(f"converting to: {output_file}")
#             logger.info(f"converting to: {output_file}")
#             hic = hicstraw.HiCFile(in_file)
#             print(hic.getChromosomes())
#             print(hic.getGenomeID())
#             print(hic.getResolutions())
#             temp = str(chr)
#             if chr_size.startswith("mm"):
#                 chr = "chr"+temp
#             bed = hicstraw.straw(d_type, norm, in_file,
#                                  chr, chr, 'BP', res)
#             if chr_size.startswith("hg"):
#                 chr = "chr"+temp
#             mat = bed2mat(bed, chrom_size[chr], res)
#             print(f"saving: {output_file}")
#             logger.info(f"saving: {output_file}")
#             # np.savetxt(output_file, mat, delimiter="\t", fmt="%.4f")
#             np.save(output_file, mat)
#             region(output_file, mat.shape[0], "chr"+str(temp), res)
#             print(f"File saved to: {output_file}")
#             logger.info(f"File saved to: {output_file}")
#             total_running_time = round(time.time() - start_time, 2)
#             print(f"Total time (seconds) taken: {total_running_time}")
#             logger.info(f"Total time (seconds) taken: {total_running_time}")


# def region(file, bins, chr, resol=10000):
#     print(f"Bin Size: {bins}")
#     start = 0
#     end = start+resol
#     with open(f"{file}_region.bed", "w") as outfile:
#         for bin in range(0, bins):
#             columns = [chr, str(start), str(end)]
#             line = '\t'.join(columns) + '\n'
#             outfile.write(line)
#             start = end
#             end = start+resol


# def to_topdom(contact_matrix, output_file, chr, resol):
#     print(f"Converting...")
#     n = contact_matrix.shape[0]
#     start_positions = np.arange(0, resol * n, resol)
#     end_positions = start_positions + resol
#     chrom = [chr]*n
#     topdom_data = pd.DataFrame({
#         "chrom": chrom,
#         "start": start_positions,
#         "end": end_positions
#     })
#     topdom_data = pd.concat(
#         [topdom_data, pd.DataFrame(contact_matrix)], axis=1)
#     topdom_data.to_csv(output_file, sep="\t",
#                        index=False, header=False)
#     print(f"Writing > {output_file}")


BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data"
# CHR_SIZE_FILE = ["mm9.chrom.sizes", "hg19.chrom.sizes"]
# FILENAMES = ["GSE63525_CH12-LX_combined_30.hic",
#              "GSE63525_GM12878_insitu_primary_replicate_combined_30.hic"]
# FILENAME_PREFIX = ["ch12lx", "gm12878_combined"]

CHR_SIZE_FILE = ["mm9.chrom.sizes"]
FILENAMES = ["GSE63525_CH12-LX_combined_30.hic"]
FILENAME_PREFIX = ["ch12lx"]

# CHROMS = [[2, 4, 6, 8, 10, 12, 14, 16, 18], ["1", "3", "5", "7", "9", "11", "13", "15",
#     "17", "19", "21"]]
CHROMS = [[18]]
RESOLS = [[10000, 5000]]
# RESOLS = [[10000, 5000], [10000, 5000]]

# if __name__ == "__main__":
#     for filename, chroms, resls, chr_size, prefix in zip(FILENAMES, CHROMS, RESOLS, CHR_SIZE_FILE, FILENAME_PREFIX):
#         to_square_matrix(chrom_size_file=f"{BASE_PATH}/{chr_size}", in_file=F"{BASE_PATH}/{filename}", out_path=f"{BASE_PATH}/matrix/",
#                          out_prefix=prefix, chroms=chroms, resols=resls)


if __name__ == "__main__":
    for filename in ["mouse_naiev_10000.cool", "mouse_th1_10000.cool", "mouse_th17_10000.cool"]:
        cool_to_matrix(
            f"/home/mohit/Documents/project/EmbedTAD/data/bio_analysis", filename, 2)
