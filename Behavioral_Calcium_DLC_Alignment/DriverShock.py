from Session import Session
import time
from pathlib import Path
import os
import glob
from builtins import AttributeError
import sys

import pandas as pd

sys.path.insert(0, "/home/rory/Rodrigo/Behavioral_Calcium_DLC_Analysis")


class Driver:

    def run_one_session_one_neuron():
        list_of_combos_we_care_about = [
            "Block_Choice Time (s)",
            "Block_Learning Stratergy_Choice Time (s)",
            "Block_Omission_Choice Time (s)",
            "Block_Reward Size_Choice Time (s)",
            "Block_Reward Size_Shock Ocurred_Choice Time (s)",
            "Block_Shock Ocurred_Choice Time (s)",
            "Block_Trial Type_Choice Time (s)",
            "Shock Ocurred_Choice Time (s)",
            "Trial Type_Choice Time (s)",
            "Trial Type_Reward Size_Choice Time (s)",
            "Block_Trial Type_Omission_Choice Time (s)",
            "Block_Trial Type_Reward Size_Choice Time (s)",
            "Block_Trial Type_Shock Ocurred_Choice Time (s)",
            "Block_Trial Type_Win or Loss_Choice Time (s)",
            "Trial Type_Shock Ocurred_Choice Time (s)",
            "Win or Loss_Choice Time (s)",
            "Block_Win or Loss_Choice Time (s)",
            "Learning Stratergy_Choice Time (s)",
            "Omission_Choice Time (s)",
            "Reward Size_Choice Time (s)",
        ]
        try:
            SESSION_PATH = (
                r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-6/Shock Test NEW_SCOPE"
            )

            session_1 = Session(SESSION_PATH)

            # now make individual neuron objects for each of the columns
            # print("Dict of all neurons in session: ", session_1.neurons)

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
                """            neuron_obj.add_aligned_dff_traces(
                        "Choice Time (s)",
                        half_of_time_window=10,
                        trial_type="Trial Type",
                        reward_size="Reward Size",
                    )"""
                neuron_obj.add_aligned_dff_traces(
                    "Shock Time (s)",
                    half_of_time_window=5,
                    shock_intensity="Shock Intensity (mA)"
                )
                # time always goes first, everything else goes in order (time window not included in name)
                # print(neuron_obj.categorized_dff_traces)
                number_of_event_traces = 0
                start = time.time()
                for (
                    event_name,
                    eventraces,
                ) in neuron_obj.get_categorized_dff_traces().items():
                    print(
                        "Event traces name: ",
                        eventraces.get_event_traces_name(),
                    )
                    if (
                        "_Choice Time (s)" != eventraces.get_event_traces_name()
                        and "_Start Time (s)" != eventraces.get_event_traces_name()
                        and "_Collection Time (s)" != eventraces.get_event_traces_name()
                        and "_Shock Time (s)" != eventraces.get_event_traces_name()
                    ):  # omitting an anomaly, we don't want just times to be a grouping
                        is_eventname_in_list_we_care_about = [
                            ele
                            for ele in list_of_combos_we_care_about
                            if (ele == eventraces.get_event_traces_name())
                        ]

                        if bool(is_eventname_in_list_we_care_about) == True:
                            """print(
                                f"WE CARE ABOUT: {eventraces.get_event_traces_name()}"
                            )"""
                            number_of_event_traces += 1
                            """print(
                                    "Event trace number: ",
                                    number_of_event_traces,
                                )"""
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
                        else:
                            """print(
                                f"WE DON'T CARE ABOUT: {eventraces.get_event_traces_name()}"
                            )"""
                            pass
                print("Time taken for %s: %s" %
                      (cell_name, time.time() - start))
                # break  # <- FOR RUNNING ONE NEURON
        except Exception as e:
            print(
                "NO ABET TABLE FOUND, SO SINGLE CELL ALIGNMENT & ANALYSIS CAN'T BE DONE!"
            )
            print(e)


if __name__ == "__main__":
    Driver.run_one_session_one_neuron()
