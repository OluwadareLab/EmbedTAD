from et_logger import *
from embed_tad import *

RESOLUTIONS = [40000]
CHROMOSOMS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

PREFIX = "HPTAD_"
MATRIX_FILEPATH = "/home/mohit/Documents/project/EmbedTAD/data/matrix/"
OUTPUT_FILEPATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/"

for resol in RESOLUTIONS:
    for chr in CHROMOSOMS:
        input = MATRIX_FILEPATH + PREFIX + \
            str(resol) + "_chr" + str(chr)+".mat"
        output_file = OUTPUT_FILEPATH + PREFIX + str(resol) + "_chr" + str(chr)
        logger = base_logger(output_file)
        clustering(logger=logger, input_file=input,
                   resolution=resol, output_file=output_file)