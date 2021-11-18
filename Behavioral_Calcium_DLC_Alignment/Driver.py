from builtins import AttributeError
import sys

import pandas as pd

sys.path.insert(0, "/home/rory/Rodrigo/Behavioral_Calcium_DLC_Analysis")
import glob
import os
from pathlib import Path
import time

from Session import Session


class Driver:
    def main():
        """11/12/21 : editing it so it runs through all the sessions in a mouse and ignores the
        sessions in which already have been processed

        Returns:
        dff traces for a given time window for each accepted cell for each session in each mouse, for a given PTP Inscopix folder
        """
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

        MASTER_ROOT = Path(r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#1")
        mouse_paths = [
            os.path.join(MASTER_ROOT, dir)
            for dir in os.listdir(MASTER_ROOT)
            if os.path.isdir(os.path.join(MASTER_ROOT, dir)) and dir.startswith("BLA")
        ]
        for mouse_path in mouse_paths:
            print("CURRENT MOUSE PATH: ", mouse_path)

            MOUSE_PATH = Path(mouse_path)

            ### TODO: Have this loop through all sessions for each mouse
            session_paths = [
                os.path.join(MOUSE_PATH, dir)
                for dir in os.listdir(MOUSE_PATH)
                if os.path.isdir(os.path.join(MOUSE_PATH, dir))
                and dir.startswith("Session")
            ]

            for session_path in session_paths:

                try:

                    session_1 = Session(session_path)
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
                        """            neuron_obj.add_aligned_dff_traces(
                            "Choice Time (s)",
                            half_of_time_window=10,
                            trial_type="Trial Type",
                            reward_size="Reward Size",
                        )"""
                        neuron_obj.add_aligned_dff_traces(
                            "Choice Time (s)",
                            half_of_time_window=10,
                            block="Block",
                            trial_type="Trial Type",
                            rew_size="Reward Size",
                            shock="Shock Ocurred",
                            omission="Omission",
                            win_loss="Win or Loss",
                            learning_strat="Learning Stratergy",
                        )
                        # time always goes last, everything else goes in order (time window not included in name)
                        # print(neuron_obj.categorized_dff_traces)
                        number_of_event_traces = 0
                        start = time.time()
                        for (
                            event_name,
                            eventraces,
                        ) in neuron_obj.get_categorized_dff_traces().items():
                            """print(
                                "Event traces name: ",
                                eventraces.get_event_traces_name(),
                            )"""
                            if (
                                "_Choice Time (s)" != eventraces.get_event_traces_name()
                                and "_Start Time (s)"
                                != eventraces.get_event_traces_name()
                                and "_Collection Time (s)"
                                != eventraces.get_event_traces_name()
                            ):  # omitting an anomaly
                                is_eventname_in_list_we_care_about = [
                                    ele
                                    for ele in list_of_combos_we_care_about
                                    if (ele == eventraces.get_event_traces_name())
                                ]

                                if bool(is_eventname_in_list_we_care_about) == True:
                                    print(
                                        f"WE CARE ABOUT: {eventraces.get_event_traces_name()}"
                                    )
                                    number_of_event_traces += 1
                                    print(
                                        "Event trace number: ", number_of_event_traces
                                    )
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
                                    print(
                                        f"WE DON'T CARE ABOUT: {eventraces.get_event_traces_name()}"
                                    )
                        print(
                            "Time taken for %s: %s" % (cell_name, time.time() - start)
                        )
                except:
                    print(
                        "NO ABET TABLE FOUND, SO SINGLE CELL ALIGNMENT & ANALYSIS CAN'T BE DONE!"
                    )
                    pass

        # Does it identify the ABET file for this session? yes
        # print(session_1.behavioral_df.head())

    def main2():
        """11/12/21 : editing it so it runs through all the sessions in a mouse and ignores the
        sessions in which already have been processed

        Returns:
        dff traces for a given time window for each accepted cell for each session in each mouse, for a given PTP Inscopix folder
        """

        session_path = r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-5/Session-20210623-093122_BLA-Insc-5_PR_D2_NEW_SCOPE"
        session_1 = Session(session_path)
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
            """            neuron_obj.add_aligned_dff_traces(
                "Choice Time (s)",
                half_of_time_window=10,
                trial_type="Trial Type",
                reward_size="Reward Size",
            )"""
            neuron_obj.add_aligned_dff_traces(
                "Choice Time (s)",
                half_of_time_window=10,
                block="Block",
                trial_type="Trial Type",
                rew_size="Reward Size",
                shock="Shock Ocurred",
                omission="Omission",
                win_loss="Win or Loss",
                learning_strat="Learning Stratergy",
            )
            # time always goes last, everything else goes in order (time window not included in name)
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
                ):  # omitting an anomaly
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
            print("Time taken for %s: %s" % (cell_name, time.time() - start))
            break  # for just doing it on one neuron

        # Does it identify the ABET file for this session? yes
        # print(session_1.behavioral_df.head())


if __name__ == "__main__":
    Driver.main()
