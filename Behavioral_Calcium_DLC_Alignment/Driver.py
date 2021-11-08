import sys

import pandas as pd

sys.path.insert(0, "/home/rory/Rodrigo/Behavioral_Calcium_DLC_Analysis")
import glob
import os
from pathlib import Path

from Session import Session


class Driver:
    def main():

        MOUSE_PATH = Path(r"/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6")

        ### TODO: Have this loop through all sessions for each mouse

        session_1 = Session(
            r"/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1"
        )
        # print(session_1.get_dff_traces().head())
        # now make individual neuron objects for each of the columns
        print("Dict of all neurons in session: ", session_1.neurons)

        # Go into one neuron obj from the neuron dict, call its method that returns a list
        # but only getting values 0-10 (exclusive)

        # Looping into all neuron objects in neurons dict from session
        for cell_name, neuron_obj in session_1.get_neurons().items():
            print(
                "################################ Cell name:",
                cell_name,
                " ################################",
            )
            # print(neuron_obj.get_sample_dff_times())
            # print(neuron_obj.get_dff_trace())
            neuron_obj.add_aligned_dff_traces(
                "Choice Time (s)",
                half_of_time_window=10,
                trial_type="Trial Type",
                reward_size="Reward Size",
            )
            # print(neuron_obj.categorized_dff_traces)
            number_of_event_traces = 0
            for (
                event_name,
                eventraces,
            ) in neuron_obj.get_categorized_dff_traces().items():
                print("Event traces name: ", eventraces.get_event_traces_name())
                number_of_event_traces += 1
                print("Number of event traces: ", number_of_event_traces)
                # print(eventraces.get_dff_traces_of_neuron())
                # but can it pull the abet data for every event trace?
                # print(eventraces.get_abet())
                """now I have abet and dff ready to go, now write
                a function in EventTraces to make this processed table
                for this neuron depending on the input parameters"""
                # testing groupby
                eventraces.process_dff_traces_by()  # returns path of csv
                # avg_cell_eventrace(csv_path)
                # PLOT

        # Does it identify the ABET file for this session? yes
        # print(session_1.behavioral_df.head())


if __name__ == "__main__":
    Driver.main()
