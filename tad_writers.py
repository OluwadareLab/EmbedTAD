import os
import csv

def init_csv_file(file, headers):
    if not os.path.exists(file):
        score_file = open(file, "w", newline="")
        score_file_writer = csv.writer(score_file)
        score_file_writer.writerow(headers)
        score_file.close()


def write_csv_file(file, row):
    if os.path.exists(file):
        score_file = open(file, "a", newline="")
        score_file_writer = csv.writer(score_file)
        score_file_writer.writerow(row)
        score_file.close()


def write_tads(tads, file):
    tads.to_csv(file + ".tsv", sep="\t", header=False, index=False)


def write_tad_quality(tad_quality, file):
    with open(file+"_tq.txt", "w") as file:
        file.write(f"TAD Quality: {tad_quality}\n")
