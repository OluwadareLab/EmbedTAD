import logger as log
import cuda_pipeline as cuda_pip

import warnings

warnings.simplefilter(action='ignore')

RESOLUTIONS = [[10000, 5000,], [10000, 5000]]
CHROMOSOMS = [[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
              [2, 4, 6, 8, 10, 12, 14, 16, 18]]
IN_PREFIXS = ["gm12878_combined", "ch12lx"]
OUT_PREFIXS = ["cuda_gm12878_", "cuda_ch12lx_"]
MATRIX_FILEPATH = "/home/mohit/Documents/project/EmbedTAD/data/matrix/"
OUTPUT_FILEPATHS = ["/home/mohit/Documents/project/EmbedTAD/data/resutls/raw/gm12878/",
                    "/home/mohit/Documents/project/EmbedTAD/data/resutls/raw/ch12lx/"]

# for file in ["mouse_th1_10000_chr2"]:
input = f"/home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/naive_10000_chr2.txt"
output = f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/naive_10000_chr2"
logger = log.base_logger(output)
cuda_pip.clustering(logger=logger, input_file=input,
                    resol=10000, output_file=output, norm=True)

input = f"/home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/th17_10000_chr2.txt"
output = f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th17_10000_chr2"
logger = log.base_logger(output)
cuda_pip.clustering(logger=logger, input_file=input,
                    resol=10000, output_file=output, norm=True)

input = f"/home/mohit/Documents/project/embed_tad/data/raw/mus_gse210418/th1_10000_chr2.txt"
output = f"/home/mohit/Documents/project/embed_tad/data/results/gpu/mus_gse210418/th1_10000_chr2"
logger = log.base_logger(output)
cuda_pip.clustering(logger=logger, input_file=input,
                    resol=10000, output_file=output, norm=True)

# for in_p, resols, chroms, out_p, out_path in zip(IN_PREFIXS, RESOLUTIONS, CHROMOSOMS, OUT_PREFIXS, OUTPUT_FILEPATHS):
#     for resol in resols:
#         for chr in chroms:
#             input = f"{MATRIX_FILEPATH}{in_p}{resol}_chr{chr}.txt"
#             output = f"{out_path}{out_p}_{resol}_chr{chr}"
#             logger = log.base_logger(output)
#             cuda_pip.clustering(logger=logger, input_file=input,
#                                 resol=resol, output_file=output, norm=True)


# for i in range(2, 3, 1):
#     for resol in RESOLUTIONS[i]:
#         for chr in CHROMOSOMS[i]:
#             input = MATRIX_FILEPATH + IN_PREFIXS[i] + \
#                 str(resol) + "_chr" + str(chr)+".txt"
#             output_file = OUTPUT_FILEPATHS[i] + OUT_PREFIXS[i] + \
#                 str(resol) + "_chr" + str(chr)
#             logger = log.base_logger(output_file)
#             cuda_pip.clustering(logger=logger, input_file=input,
#                                 resol=resol, output_file=output_file, norm=True)