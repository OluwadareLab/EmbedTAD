import logging
import warnings
warnings.simplefilter(action='ignore')


def base_logger(file):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=file+".log", format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

    return logger
