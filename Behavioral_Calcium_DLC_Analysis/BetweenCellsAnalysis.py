from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import glob, os
from typing import List, Optional
from numpy.core.fromnumeric import mean
import pandas as pd
import seaborn as sns
import os.path as path
from scipy import stats


def walk(top, topdown=True, onerror=None, followlinks=False, maxdepth=None):
    islink, join, isdir = path.islink, path.join, path.isdir

    try:
        names = os.listdir(top)
    except OSError as err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs

    if maxdepth is None or maxdepth > 1:
        for name in dirs:
            new_path = join(top, name)
            if followlinks or not islink(new_path):
                for x in walk(
                    new_path,
                    topdown,
                    onerror,
                    followlinks,
                    None if maxdepth is None else maxdepth - 1,
                ):
                    yield x
    if not topdown:
        yield top, dirs, nondirs


def find_paths_endswith(root_path, endswith) -> List:

    files = glob.glob(
        os.path.join(root_path, "**", "*%s") % (endswith),
        recursive=True,
    )

    return files


def find_paths_startswith(root_path, startswith) -> List:

    files = glob.glob(
        os.path.join(root_path, "**", "%s*") % (startswith),
        recursive=True,
    )

    return files


def find_paths_conditional_endswith(
    root_path, og_lookfor: str, cond_lookfor: str
) -> List:

    all_files = []

    for root, dirs, files in os.walk(root_path):

        if cond_lookfor in files:
            # acquire the trunc file
            file_path = os.path.join(root, cond_lookfor)
            # print(file_path)
            all_files.append(file_path)
        elif cond_lookfor not in files:
            # acquire the og lookfor
            file_path = os.path.join(root, og_lookfor)
            all_files.append(file_path)

    return all_files


# For an individual cell
def indv_events_spaghetti_plot(lst_of_indv_event_traces_of_cell):
    for csv_path in lst_of_indv_event_traces_of_cell:
        print(csv_path)
        try:
            new_path = csv_path.replace("plot_ready.csv", "spaghetti_plot.png")
            df = pd.read_csv(csv_path)
            number_of_events = df.shape[0]
            # print("df # rows: ", len(df))
            df_without_eventcol = df.loc[:, df.columns != "Event #"]
            # print(df_without_eventcol.head())
            just_event_col = df.loc[:, df.columns == "Event #"]
            # print(just_event_col.head())
            df_no_eventcol_mod = standardize(df_without_eventcol)
            df_no_eventcol_mod = gaussian_smooth(df_without_eventcol)
            # print(df_no_eventcol_mod.head())

            df = pd.concat([just_event_col, df_no_eventcol_mod], axis=1)
            df = df.T

            new_header = df.iloc[0]  # first row
            df = df[1:]  # don't include first row in new df
            df.columns = new_header
            # print(df.head())

            x = list(df.index)
            # print(x)

            # print(list(df.columns))
            for col in df.columns:
                print("col: ", col)
                if col != "Event #":
                    plt.plot(x, list(df[col]), label=col)

            plt.title("All Events for Cell (n=%s)" % (number_of_events))
            plt.locator_params(axis="x", nbins=20)
            plt.savefig(new_path)
            plt.close()

        except ValueError as e:
            print("VALUE ERROR:", e)
            pass


def heatmap(
    file_path,
    unknown_time_min,
    unknown_time_max,
    reference_pair: dict,
    hertz: int,
    cols_to_plot: Optional[List[str]] = None,
    cmap: str = "coolwarm",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    **heatmap_kwargs,
):

    try:
        new_path = file_path.replace(".csv", "_heatmap_baseline-10_-1_gauss1.5.png")
        # new_path_csv = file_path.replace(".csv", "_heatmap_baseline-10_-1_gauss2.csv")
        df = pd.read_csv(file_path)
        # DONT TRANSPOSE FOR STANDARDIZATION
        df = custom_standardize(
            df, unknown_time_min, unknown_time_max, reference_pair, hertz
        )
        # TRANSPOSE FOR STANDARDIZATION
        df = gaussian_smooth(df.T)
        if cols_to_plot is not None:
            df = df[cols_to_plot]

        print(df.head())
        # df.to_csv(new_path_csv, index=False)
        # BUT DONT TRANSOSE AGAIN
        sns.heatmap(df, vmin=vmin, vmax=vmax, cmap=cmap, **heatmap_kwargs)
        plt.savefig(new_path)
        plt.close()
    except ValueError as e:
        print("VALUE ERROR:", e)
        print(f"VALUE ERROR FOR {file_path} --> MAKING HEATMAP")
        pass


# For averaged dff trace of cell, across cells
def spaghetti_plot(
    file_path, unknown_time_min, unknown_time_max, reference_pair, hertz
):
    try:
        new_path = file_path.replace(".csv", "_spaghetti_baseline-10_-1_gauss1.5.png")
        df = pd.read_csv(file_path)
        # DONT TRANSPOSE FOR STANDARDIZATION
        df = custom_standardize(
            df, unknown_time_min, unknown_time_max, reference_pair, hertz
        )
        # make sure you're taking guassian by the axis=1, so by columns when using
        # .apply for this gaussian_smooth() function
        # TRANSPOSE FOR STANDARDIZATION
        df = gaussian_smooth(df.T)
        # TRANSPOSE BACK FOR SPAGHETTI
        df = df.T
        x = list(df.index)
        for cell in df.columns:
            # print("cell: ", cell)
            plt.plot(x, list(df[cell]), label=cell)
        number_cells = len(df.T)
        plt.title("DF/F (n=%s)" % (number_cells))
        plt.locator_params(axis="x", nbins=20)
        plt.savefig(new_path)
        plt.close()

    except ValueError as e:

        print("VALUE ERROR:", e)
        print(f"VALUE ERROR FOR {file_path} --> MAKING SPAGHETTI")
        pass


"""
Example:
    reference_pair -> 0 seconds : 99 idx (reference is something we know already)
    hertz -> 10 Hz (10 cycles(recordings) / 1 sec)
"""


def custom_standardize(
    df, unknown_time_min, unknown_time_max, reference_pair: dict, hertz: int
):
    # print(df.head())
    for col in df.columns:
        idx_start, idx_end = convert_secs_to_idx(
            unknown_time_min, unknown_time_max, reference_pair, hertz
        )
        arr_of_focus = df[col][idx_start:idx_end]
        mean_for_cell = stats.tmean(arr_of_focus)
        stdev_for_cell = stats.tstd(arr_of_focus)
        # print(arr_of_focus)
        # print(f"Mean {mean_for_cell} for cell {col}")
        # print(stdev_for_cell)

        new_col_vals = []
        for ele in list(df[col]):
            z_value = zscore(ele, mean_for_cell, stdev_for_cell)
            new_col_vals.append(z_value)

        # print(new_col_vals[0:10])  # has nan values
        df[col] = new_col_vals  # <- not neccesary bc of the .apply function?
    return df


def zscore(obs_value, mu, sigma):
    return (obs_value - mu) / sigma


def convert_secs_to_idx(
    unknown_time_min, unknown_time_max, reference_pair: dict, hertz: int
):
    reference_time = list(reference_pair.keys())[0]  # has to come from 0
    reference_idx = list(reference_pair.values())[0]

    # first find the time difference between reference and unknown
    # Note: reference will
    idx_start = (unknown_time_min * hertz) + reference_idx
    idx_end = (unknown_time_max * hertz) + reference_idx + 1
    # ^plus 1 bc getting sublist is exclusive
    return int(idx_start), int(idx_end)


"""def standardize(df):
    # from scipy.stats import zscore
    # ^ not specific enough for our use case

    return df.apply(zscore)"""


def gaussian_smooth(df, sigma: float = 1.5):
    from scipy.ndimage import gaussian_filter1d

    return df.apply(gaussian_filter1d, sigma=sigma, axis=0)


def main():

    ROOT_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData"

    to_look_for_originally = "all_concat_cells.csv"
    # would only look for this is the file causing the conditional statement didn't exist
    to_look_for_conditional = "all_concat_cells_truncated.csv"

    csv_list = find_paths_conditional_endswith(
        ROOT_PATH, to_look_for_originally, to_look_for_conditional
    )
    # print(csv_list)
    for count, file_path in enumerate(csv_list):

        print(f"Working on file {count}: {file_path}")

        try:
            heatmap(file_path, vmin=-2.5, vmax=2.5)
            spaghetti_plot(file_path)
        except FileNotFoundError:
            pass


def process_one_table():
    csv_path = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData/RDT D2/Shock Ocurred_Choice Time (s)/True/all_concat_cells.csv"
    heatmap(
        csv_path,
        unknown_time_min=-10.0,
        unknown_time_max=-1.0,
        reference_pair={0: 100},
        hertz=10,
        vmin=-2.5,
        vmax=2.5,
    )
    spaghetti_plot(
        csv_path,
        unknown_time_min=-10.0,
        unknown_time_max=-1.0,
        reference_pair={0: 100},
        hertz=10,
    )


if __name__ == "__main__":
    # main()
    process_one_table()
