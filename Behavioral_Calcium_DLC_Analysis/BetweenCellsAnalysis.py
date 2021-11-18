from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import glob, os
from typing import List, Optional
import pandas as pd
import seaborn as sns


def find_csv_paths(session_path, endswith) -> List:

    files = glob.glob(
        os.path.join(session_path, "**", "*%s") % (endswith),
        recursive=True,
    )

    return files


def find_csv_paths_startswith(session_path, startswith) -> List:

    files = glob.glob(
        os.path.join(session_path, "**", "%s*") % (startswith),
        recursive=True,
    )

    return files


def plot_traces(
    lst_of_concat_csv_paths,
    cols_to_plot: Optional[List[str]] = None,
    cmap: str = "coolwarm",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    **heatmap_kwargs
):
    for concat_path in lst_of_concat_csv_paths:
        try:
            new_path = concat_path.replace(
                "concat_cells.csv", "concat_heatmap_zscore2.5_gauss0.2.png"
            )
            df = pd.read_csv(concat_path)
            df = standardize(df)
            df = gaussian_smooth(df)
            if cols_to_plot is not None:
                df = df[cols_to_plot]

            sns.heatmap(
                df.transpose(), vmin=vmin, vmax=vmax, cmap=cmap, **heatmap_kwargs
            )
            plt.savefig(new_path)
            plt.close()
        except ValueError:
            pass


def spaghetti_plot_indv_events_in_cell(lst_of_indv_event_traces_of_cell):
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


def spaghetti_plot_across_avg_cell_trace(lst_of_indv_event_traces_of_cell):
    for csv_path in lst_of_indv_event_traces_of_cell:
        print(csv_path)
        try:
            new_path = csv_path.replace("concat_cells.csv", "spaghetti_plot.png")
            df = pd.read_csv(csv_path)

            df = standardize(df)
            df = gaussian_smooth(df)
            x = list(df.index)
            for cell in df.columns:
                print("cell: ", cell)
                plt.plot(x, list(df[cell]), label=cell)
            number_cells = len(df.T)
            plt.title("DF/F (n=%s)" % (number_cells))
            plt.locator_params(axis="x", nbins=20)
            plt.savefig(new_path)
            plt.close()

        except ValueError as e:
            print("VALUE ERROR:", e)
            pass


def standardize(df):
    from scipy.stats import zscore

    return df.apply(zscore)


def gaussian_smooth(df, sigma: float = 0.2):
    from scipy.ndimage import gaussian_filter1d

    return df.apply(gaussian_filter1d, sigma=sigma)


def main():
    # For a given session
    SESSION_ROOT = Path(
        r"/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1"
    )
    BETWEEN_CELL_ALIGNMENT_ROOT = os.path.join(SESSION_ROOT, "BetweenCellalignmentData")

    lst_of_concat_csv_paths = find_csv_paths(SESSION_ROOT, "concat_cells.csv")
    plot_traces(lst_of_concat_csv_paths, vmin=-2.5, vmax=2.5)


def main2():
    # For a given session
    SESSION_ROOT = Path(
        r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-5/Session-20210510-093930_BLA-Insc-5_RM_D1"
    )

    lst_of_indv_event_traces_of_cell = find_csv_paths_startswith(
        SESSION_ROOT, "plot_ready.csv"
    )
    spaghetti_plot_indv_events_in_cell(lst_of_indv_event_traces_of_cell)


def main3():
    # For a given session
    SESSION_ROOT = Path(
        r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-5/Session-20210510-093930_BLA-Insc-5_RM_D1"
    )
    BETWEEN_CELL_ALIGNMENT_ROOT = os.path.join(SESSION_ROOT, "BetweenCellAlignmentData")

    lst_of_concat_csv_paths = find_csv_paths(SESSION_ROOT, "concat_cells.csv")
    plot_traces(lst_of_concat_csv_paths, vmin=-2.5, vmax=2.5)

    lst_of_indv_event_traces_of_cell = find_csv_paths_startswith(
        SESSION_ROOT, "plot_ready.csv"
    )

    spaghetti_plot_indv_events_in_cell(lst_of_indv_event_traces_of_cell)


def main4():
    # For a given session
    SESSION_ROOT = Path(
        r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-5/Session-20210510-093930_BLA-Insc-5_RM_D1"
    )

    lst_of_indv_event_traces_of_cell = find_csv_paths_startswith(
        SESSION_ROOT, "concat_cells.csv"
    )
    spaghetti_plot_across_avg_cell_trace(lst_of_indv_event_traces_of_cell)


if __name__ == "__main__":
    # main()
    main4()
