from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import glob, os
from typing import List, Optional
import pandas as pd
import seaborn as sns


def concatenated_csvs_paths(session_path, endswith) -> List:

    files = glob.glob(
        os.path.join(session_path, "**", "*%s") % (endswith),
        recursive=True,
    )

    return files


def find_non_avg_cell_event_csvs(session_path, endswith) -> List:
    pass


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
                "concat_cells.csv", "concat_heatmap_zscore2.5_fauss_sigma.png"
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

    lst_of_concat_csv_paths = concatenated_csvs_paths(SESSION_ROOT, "concat_cells.csv")
    plot_traces(lst_of_concat_csv_paths, vmin=-2.5, vmax=2.5)


main()
