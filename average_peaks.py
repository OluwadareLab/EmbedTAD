import pandas as pd
import math


def get_average_peaks(tads: pd.DataFrame, ref_file: pd.DataFrame, chr_sizes: pd.DataFrame, chr: str, resol: int, window: int = 0):
    chr_size = int(chr_sizes[chr_sizes.iloc[:, 0] == chr][1])
    start_pixel = 0
    end_pixel = math.ceil(chr_size/resol)*resol

    # extract ref values
    chr_ref_file = ref_file.loc[ref_file.iloc[:, 1] == chr, [2, 3]]
    chr_ref_file.columns = ["start", "end"]

    # Create indexed count
    average_counts = pd.DataFrame()
    average_counts["idx"] = ""
    average_counts["pixel"] = ""
    average_counts["count"] = ""
    str_pxl = -500
    lim = int(500/(resol/1000))
    for i in range(-lim, lim+1, 1):
        average_counts.loc[len(average_counts.index)] = [i, str_pxl, 0]
        str_pxl = str_pxl+(resol/1000)

    # Generate bins for every new boundaries
    boundaries = 0
    for i in range(len(tads) - 1):
        row_1 = tads.iloc[i][1]
        row_2 = tads.iloc[i+1][0]
        if row_1 == row_2:
            row_2 = row_2 + resol
        get_peaks(row_1, row_2, start_pixel, end_pixel,
                  resol, lim, chr_ref_file, average_counts, window)
        boundaries = boundaries + 1

    average_counts["count"] = average_counts["count"]/boundaries
    return average_counts


def get_peaks(start, end, start_pixel, end_pixel, resol, lim, chr_ref_file, average_counts, window):
    boundaries = pd.DataFrame()
    boundaries["idx"] = ""
    boundaries["start"] = ""
    boundaries["end"] = ""
    boundaries.loc[len(boundaries.index)] = [
        0, start if start >= 0 else start_pixel, end if end <= end_pixel else end_pixel]
    flag = 0
    n_idx = -1
    p_idx = 1
    while n_idx >= -lim or p_idx <= lim:
        tmp = start
        start = start-resol
        if start >= start_pixel:
            boundaries.loc[len(boundaries.index)] = [n_idx, start, tmp]
            n_idx = n_idx-1
            flag = flag + 1
        tmp = end
        end = end+resol
        if end <= end_pixel:
            boundaries.loc[len(boundaries.index)] = [p_idx, tmp, end]
            p_idx = p_idx+1
            flag = flag + 1
        if flag > 0:
            flag = 0
        else:
            break
    for j in range(len(boundaries)):
        window = int(resol/1000) if window == 0 else window
        row = boundaries.iloc[j]
        idx = row["idx"]
        lower_bound = row["start"] - window
        upper_bound = row["end"] + window
        count = len(chr_ref_file[(chr_ref_file["start"] >= lower_bound) & (
            chr_ref_file["end"] <= upper_bound)])
        average_counts.loc[average_counts['idx'] == idx, "count"] += count
