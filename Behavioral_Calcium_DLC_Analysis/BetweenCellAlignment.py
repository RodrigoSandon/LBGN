import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
import os, glob
from pathlib import Path
from typing import List
import json

"""" Note: We are modulating this analysis by separating analysis code with setting up code.
This is the simplest type of modularity so that I won't have to edit code that got it to that point in first place.
However, this modularity has it's drawbacks: Still need to go back and forth between code to setup another analysis
only in the case we want to derive some other metric for each cell, for a given time window, for any given event combo
(which would require editing of setting up data). Either way this should be the lowest data we get into.
"""


def find_avg_dff_of_cell_for_event(session_path, endswith):

    files = glob.glob(
        os.path.join(session_path, "**", "*%s") % (endswith),
        recursive=True,
    )

    return files


def create_dict_of_what_csvs_to_concat(
    lst_of_avg_plot_rdy_csv_paths, bw_cell_data_path
):
    event_dict = {}
    """
    d =
    {
    trial type reward size choice time: { 
                                        combo: [csv paths for every cell],
                                        combo: [csv paths for every cell]
                                        },
    trial type reward size choice time: { 
                                        combo: [csv paths for every cell],
                                        combo: [csv paths for every cell]
                                        }
    }
    """
    for path in lst_of_avg_plot_rdy_csv_paths:
        eventname = path.split("/")[9]
        if eventname not in event_dict:
            event_dict[eventname] = {}

    # now event_dict with empty dict as value (should be only 2 k:v pairs)
    # for every  event, add new k:v pairs corresponding to the combos found in them
    for key in event_dict:
        # now iterate through paths again but only find combos for paths that contain this event name
        for path in lst_of_avg_plot_rdy_csv_paths:
            event_name = path.split("/")[9]
            combo_name = path.split("/")[10]
            if event_name == key:  # event names match
                # print(combo_name, key)
                # create an empty cell_dict, this is where all the cell avg dff traces are going to go
                # get the combo, add as many combos as there are seen, but only if have never seen that combo before
                if combo_name not in event_dict[key]:

                    event_dict[key][combo_name] = {}

    # now ready to add on k:v pairs of cell avg dff traces for every combo, within every event_name
    for event in event_dict:
        for combo in event_dict[event]:
            for path in lst_of_avg_plot_rdy_csv_paths:
                event_name = path.split("/")[9]
                combo_name = path.split("/")[10]
                cell_name = path.split("/")[8]
                if event_name == event and combo_name == combo:
                    if cell_name not in event_dict[event_name][combo_name]:
                        df = pd.read_csv(path)
                        event_dict[event_name][combo_name][cell_name] = df[
                            cell_name
                        ].tolist()
    """"This function also concatenates cells"""
    for event in event_dict:
        for combo in event_dict[event]:
            # now have all cells for combo, now just combine them all to one csv
            # print(event_dict[event][combo])
            concatenated_cell_avg_dff_for_combo_within_event = pd.DataFrame.from_dict(
                event_dict[event][combo]
            )
            new_path = os.path.join(bw_cell_data_path, event, combo)
            os.makedirs(new_path, exist_ok=True)
            concatenated_cell_avg_dff_for_combo_within_event.to_csv(
                os.path.join(new_path, "concat_cells.csv"), index=False
            )

    # print(json.dumps(event_dict, sort_keys=False, indent=4))
    """with open(os.path.join(bw_cell_data_path, "overall_d.txt"), "w") as f:
        json.dump(event_dict, f)"""

    """ print this dict to check, then as you iterate through the combos within
    event name, iterate through the csv paths. open paths as dfs, and add them into
    a new dict as {cell_name : avg dff traces, cell_name : avg dff traces}. from there,
    within that same combo directory, save this dict into csv and make a new file
    called AnalysisUtilities.py, write a func in this file that takes this csv file and
    plots it using matplotlib (spend more time on matplotlib this time), save this plot into the
    combo directory with a proper name of file adn try to get is to look like that figure."""


def main():
    SESSION_PATH = Path(
        r"/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1"
    )

    lst_of_avg_plot_rdy_csv_paths = find_avg_dff_of_cell_for_event(
        SESSION_PATH, "avg_plot_ready.csv"
    )
    # print(*lst_of_avg_plot_rdy_csv_paths, sep="\n")
    bw_cell_alignment_folder_name = "BetweenCellAlignmentData"
    bw_cell_data_path = os.path.join(SESSION_PATH, bw_cell_alignment_folder_name)

    create_dict_of_what_csvs_to_concat(lst_of_avg_plot_rdy_csv_paths, bw_cell_data_path)


main()
