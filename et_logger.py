import logging

def base_logger(file):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=file+"_embed_tad.log", format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    return logger