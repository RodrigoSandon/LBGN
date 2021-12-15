from typing import List
import pandas as pd
import numpy as np
import glob
import os


def find_paths_startswith(root_path, startswith) -> List:

    files = glob.glob(
        os.path.join(root_path, "**", "%s*") % (startswith),
        recursive=True,
    )

    return files


def main():
    """
    Functionalities:
    1) Returns list of all plot ready csv file paths, example:

    +---------+----------+----------+----------+----------+
    | Event # | -10      | -9.9     | -9.8     | -9.7     |...
    +---------+----------+----------+----------+----------+
    | Event 1 | 1.25548  | 2.172035 | 3.490741 | 3.742469 |...
    +---------+----------+----------+----------+----------+
    | Event 2 | 2.234204 | 3.117542 | 2.026499 | 4.696948 |...
    +---------+----------+----------+----------+----------+
    | Event 3 | 4.770984 | 4.456681 | 5.656993 | 4.127113 |...
    +---------+----------+----------+----------+----------+

    For every mouse:
        For every session type:
            For every cell:
                For every event category:
                    For every event type:
                        For every row (event) in plot_ready.csv:
                            For 1000 times:
                                Shuffle the row of this event

                        avg_for_cell = { cell_name : []}
                        For every column series (dff traces for all events under that time point):
                            avg_for_cell[cell_name].append(avg of column series)

                        avg_for_cell to DataFrame
                        avg_for_cell to csv

    Run BetweenCellAlignment.py to get the concatenated traces of cells for each event type (will look for
    the avg shuffled traces of each cell for every event (avg_plot_ready.csv:

        +----------------+
        | C01            |
        +----------------+
        | 6.0267928625   |
        +----------------+
        | 5.748872253125 |
        +----------------+
        | 6.10643181875  |
        +----------------+
        | 5.942177175    |
        +----------------+
                .
                .
                .

    ))

    Once have concatenated cells from running BetweenCellAlignment.py like so:

    +------------------+-------------------+-------------------+
    | BLA-Insc-2_C01   | BLA-Insc-2_C02    | BLA-Insc-5_C01    |...
    +------------------+-------------------+-------------------+
    | 1.5908035972973  | 0.903808762162162 | 0.395520983       |...
    +------------------+-------------------+-------------------+
    | 1.85934741910811 | 1.16783503918919  | 0.554314586666667 |...
    +------------------+-------------------+-------------------+
    | 1.67148849513513 | 1.11240769783784  | 0.676555127666666 |...
    +------------------+-------------------+-------------------+
    | 1.74423583540541 | 0.962307342432432 | 0.814232835666667 |...
    +------------------+-------------------+-------------------+

    For every session type:
        For every event category:
            For every event type:
                posActive = []
                negActive = []
                neutral = []
                For every column (avg cell trace):
                    upperSD = mean of shuffled dff list (entire window) + (how many stdevs u care about * stdev)
                    lowerSD = mean of shuffled dff list (entire window) - (how many stdevs u care about * stdev)
                    # so ig 1 stdev is more of a unit of the mean for that pop rather than a unit on its own?

                    empirical_response = mean of subwindow (unshuffled) <- need to open unshuffled all_concat_cells.csv for this
                    if empirical_response > upperSD:
                        posActive.append(column)
                    elif empirical_response < lowerSD:
                        negActive.append(column)
                    else:
                        neutral.append(column)
                d = {
                    "+ Active Cells": len(posActive),
                    "- Active Cells": len(negActive),
                    "Neutral Cells": len(neutral)
                }

                #to help name the path for the output of this program
                replace_name_prefix = Utilities.make_replace_name_suffix_prefix(
                    self.standardize, self.smooth)

                #saves pie plot to a given path
                Utilities.pie_chart(self.csv_path, f"Sigma Difference Shuffled vs Unshuffled (n={number_cells})", list(
                    d.values()), list(d.keys()), replace_name=f"{replace_name_prefix}_pie_1000shuffled.png")









    """

    CONCAT_CELLS_PATH = r"/Users/rodrigosandon/Documents/GitHub/LBGN/SampleData/truncating_bug/RDT D2/Shock Ocurred_Choice Time (s)/True/all_concat_cells.csv"

    CONCAT_CELLS_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData/RDT D2/Block_Choice Time (s)/3.0/all_concat_cells.csv"

    SINGLE_CELL_EVENTS_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#1/BLA-Insc-2/Post-RDT D2/SingleCellAlignmentData/C01/Block_Choice Time (s)/1.0/plot_ready.csv"
