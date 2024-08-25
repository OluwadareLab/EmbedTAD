import logger as log
import cuda_pipeline as cuda_pip

RESOLUTIONS = [[5000, 10000], [40000]]
CHROMOSOMS = [[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
              [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]]
IN_PREFIXS = ["GM12878_insitu_primary_30_", "HPTAD_"]
OUT_PREFIXS = ["cuda_gm12878_", "cuda_hptad_"]
MATRIX_FILEPATH = "/home/mohit/Documents/project/EmbedTAD/data/matrix/"
OUTPUT_FILEPATHS = ["/home/mohit/Documents/project/EmbedTAD/data/resutls/gm12878/",
                    "/home/mohit/Documents/project/EmbedTAD/data/resutls/hptad/"]
for i in range(0, 2, 1):
    for resol in RESOLUTIONS[i]:
        for chr in CHROMOSOMS[i]:
            input = MATRIX_FILEPATH + IN_PREFIXS[i] + \
                str(resol) + "_chr" + str(chr)+".mat"
            output_file = OUTPUT_FILEPATHS[i] + OUT_PREFIXS[i] + \
                str(resol) + "_chr" + str(chr)
            logger = log.base_logger(output_file)
            cuda_pip.clustering(logger=logger, input_file=input,
                                resol=resol, output_file=output_file, normalization=False)
