import csv
import hicstraw
import numpy as np
from typing import List


def bed2mat(bed, chr_size, res=10000):
    N = int(chr_size / res)
    mat = np.zeros((N, N))
    for i in range(0, len(bed), 1):
        mat[int(bed[i].binX / res), int(bed[i].binY / res)] = bed[i].counts
        mat[int(bed[i].binY / res), int(bed[i].binX / res)] = bed[i].counts

    return mat


def to_square_matrix(chrom_size_file: str, in_file: str, out_path: str, out_prefix: str, chroms: List[str], resols: List[int] = [5000], d_type: str = "observed", norm: str = "NONE"):
    print(f"converting {in_file}")
    chrom_size = {}
    with open(chrom_size_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            chrom_size[row[0]] = int(row[1])

    for res in resols:
        for chr in chroms:
            output_file = out_path + out_prefix + \
                str(res) + "_" + "chr"+str(chr) + ".mat"
            bed = hicstraw.straw(d_type, norm,
                                 in_file, chr, chr, 'BP', res)
            mat = bed2mat(bed, chrom_size["chr"+chr], res)
            print(f"saving {output_file}")
            np.savetxt(output_file, mat, delimiter=" ", fmt="%.2f")


def main():
    chrom_size_file = "/home/mohit/Documents/project/EmbedTAD/data/hg19.chrom.sizes"
    in_file = "/home/mohit/Documents/project/EmbedTAD/data/GSE63525_GM12878_insitu_primary_30.hic"
    out_path = "/home/mohit/Documents/project/EmbedTAD/data/"
    out_prefix = "GM12878_insitu_primary_30_"
    chroms = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21"]
    resols = [5000, 10000]
    to_square_matrix(chrom_size_file=chrom_size_file, in_file=in_file, out_path=out_path,
                     out_prefix=out_prefix, chroms=chroms, resols=resols)


if __name__ == "__main__":
    main()
