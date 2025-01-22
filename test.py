import logger as log
import cuda_pipeline as cuda_pip
import warnings

warnings.simplefilter(action='ignore')

for file in ["mouse_th1_10000_chr2"]:
    input = f"./test/test/gm12878_10k_chr21.txt"
    output = f"./test/test/embedtad_gm12878_10k_chr21"
    logger = log.base_logger(output)
    cuda_pip.clustering(logger=logger, input_file=input, resol=10000, output_file=output, norm=True)
