import pandas as pd


def assembler(tads: pd.DataFrame) -> pd.DataFrame:
    tads = tads.sort_values(by=['start', 'end'])
    tads.reset_index(drop=True, inplace=True)

    # tads.to_csv(f"/home/mohit/Documents/project/embed_tad/data/results/example_input.txt",
    #             sep="\t", header=False, index=False)
    
    length = len(tads)
    for i in range(0, length-1, 1):
        count = 0
        for j in range(i+1, length, 1):
            if tads.loc[i, 'start'] <= tads.loc[j, 'start'] and tads.loc[i, 'end'] >= tads.loc[j, 'end']:
                count += 1
            else:
                if count > 1:
                    tads = tads.drop(i)
                    tads.reset_index(drop=True, inplace=True)

                elif count == 1:
                    tads = tads.drop(j-count)
                    tads.reset_index(drop=True, inplace=True)

                length = len(tads)
                count = 0
                break

    keep = [True] * len(tads)
    for i in range(len(tads) - 1):
        if (tads.loc[i, 'end'] > tads.loc[i+1, 'start']):
            tads.loc[i, 'end'] = tads.loc[i+1, 'start']-1
        if tads.loc[i+1, 'start'] <= tads.loc[i, 'start'] and tads.loc[i+1, 'end'] >= tads.loc[i, 'end']:
            keep[i] = False

    tads = tads[pd.Series(keep)].reset_index(drop=True)
    # tads.to_csv(f"/home/mohit/Documents/project/embed_tad/data/results/example_output.txt",
    #             sep="\t", header=False, index=False)
    return tads


if __name__ == "__main__":
    input_file = f"/home/mohit/Documents/project/embed_tad/data/results/exp_2_gm12878_10000_chr11.bed"
    tads = pd.read_csv(input_file, sep="\t", usecols=[0, 2], header=None)
    tads.columns = ['start', 'end']
    assembler(tads)


def get_tad_quality(start, end, tads, raw_matrix):
    quality = 0
    for tad in tads:
        quality += raw_matrix[tad[0]-1:tad[1], tad[0]-1:tad[1]].sum()
    return quality