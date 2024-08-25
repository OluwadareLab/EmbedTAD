import argparse
import os
import sys
import logger as log
import cuda_pipeline as cuda_pip
import pipeline as _pip


def arg_parser():
    parser = argparse.ArgumentParser(prog='PROG',
                                     description="Welcome to EmbedTAD.")
    parser.add_argument("-i", "--input", dest="input", type=str,
                        required=True, help="REQUIRED: Input file")
    parser.add_argument("-r", "--resolution", dest="resolution", type=int,
                        required=True, help="REQUIRED: Resolution (Option: 5000, 10000, ...)")
    parser.add_argument("-o", "--output", dest="output", type=str,
                        required=True, help="REQUIRED: Output file")
    parser.add_argument("-w", "--worker", dest="worker", type=str,
                        required=False, help="OPTIONAL: Worker (Option: CPU, GPU), Default: CPU")
    parser.add_argument("-n", "--normalization", dest="normalization", type=str,
                        required=False, help="OPTIONAL: Normalization (Option: True, False), Default: False")
    return parser.parse_args()


def main():
    args = arg_parser()
    input_file = args.input
    if not os.path.exists(input_file):
        print("Input file not found")
        sys.exit(2)

    resol = args.resolution
    if resol < 0:
        print("Invalid resolution")
        sys.exit(2)

    output_file = args.output
    if not output_file:
        print("Provide output file")
        sys.exit(2)

    worker = "cpu"
    if args.worker:
        worker = str(args.worker).lower

    norm = False
    if args.normalization:
        norm = args.normalization

    logger = log.base_logger(output_file)
    logger.info(f"______Starting Pipeline______")
    print(f"______Starting Pipeline______")
    try:
        if worker == "cpu":
            logger.info(f"Worker: CPU")
            print(f"Worker: CPU")
            _pip.clustering(logger=logger, input_file=input_file,
                           resol=resol, output_file=output_file, norm=norm)
        else:
            logger.info(f"Worker: GPU")
            print(f"Worker: GPU")
            cuda_pip.clustering(logger=logger, input_file=input_file,
                                resol=resol, output_file=output_file, norm=norm)
    except Exception as ex:
        logger.error(ex)
    logger.info(f"______Finished______")
    print(f"______Finished______")


if __name__ == "__main__":
    main()
