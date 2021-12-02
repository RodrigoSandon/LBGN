import pandas as pd
import numpy as np
import os, glob
from pathlib import Path
from BehavioralSession import BehavioralSession
from BehavioralUtilities import BehavioralUtilities


def get_session_name(path):
    name = path.split("/")[-1].replace(".csv", "")
    return name


def main(ROOT):
    """11/12/21 : going through entire mouse to check if there's an abet file that needs to be preprocessed."""
    """Give a list of the strings that have another string --> these ones don't include in analysis"""
    to_not_include_in_preprocessing = [
        "_ABET_processed.csv",
        "_ABET_GPIO_processed.csv",
        "resnet50",
    ]

    for root, dirs, files in os.walk(ROOT, topdown=True):
        roots_not_included = []
        if root.find("Session") != -1:
            # only roots with "Session"
            if (
                root.find("SingleCellAlignmentData") != -1
                or root.find("BetweenCellAlignmentData") != -1
            ):  # found
                roots_not_included.append(root)
            else:
                for name in files:
                    if name.startswith("BLA"):

                        if any(
                            os.path.join(root, name).find(session) != -1
                            for session in to_not_include_in_preprocessing
                        ):  # for any of the list elements that are not found in the current name of file
                            pass
                        else:
                            try:
                                curr_session = os.path.join(root, name)
                                print("CURRENT SESSION: ", curr_session)
                                ses_name = get_session_name(curr_session)

                                ABET_1 = BehavioralSession(
                                    ses_name,
                                    curr_session,
                                )
                                ABET_1.preprocess_csv()
                                df = ABET_1.get_df()
                                grouped_by_trialnum = df.groupby("trial_num")
                                processed_behavioral_df = grouped_by_trialnum.apply(
                                    BehavioralUtilities.process_csv
                                )  # is a new df, it's not the modified df
                                processed_behavioral_df = (
                                    BehavioralUtilities.add_winstay_loseshift_loseomit(
                                        processed_behavioral_df
                                    )
                                )
                                # Add post-hoc processing
                                processed_behavioral_df = (
                                    BehavioralUtilities.shift_col_values(
                                        processed_behavioral_df
                                    )
                                )

                                processed_behavioral_df = (
                                    BehavioralUtilities.interpolate_block(
                                        processed_behavioral_df, trails_in_block=30
                                    )
                                )
                                print("here")
                                processed_behavioral_df = (
                                    BehavioralUtilities.del_first_row(
                                        processed_behavioral_df
                                    )
                                )
                                # print(processed_behavioral_df.to_string())
                                BehavioralUtilities.verify_table(
                                    processed_behavioral_df
                                )
                                new_path = curr_session.replace(
                                    ".csv", "_ABET_processed.csv"
                                )
                                processed_behavioral_df.to_csv(
                                    new_path,
                                    index=True,
                                )
                            except Exception as e:
                                print("AN ERROR OCURRED!")
                                print(e)
                                pass


ROOT = r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#4"
main(ROOT)


def main2(curr_session):
    """11/12/21 : going through entire mouse to check if there's an abet file that needs to be preprocessed."""
    """Give a list of the strings that have another string --> these ones don't include in analysis"""

    try:

        print("CURRENT SESSION: ", curr_session)
        ses_name = get_session_name(curr_session)

        ABET_1 = BehavioralSession(
            ses_name,
            curr_session,
        )
        ABET_1.preprocess_csv()
        df = ABET_1.get_df()
        grouped_by_trialnum = df.groupby("trial_num")
        processed_behavioral_df = grouped_by_trialnum.apply(
            BehavioralUtilities.process_csv
        )  # is a new df, it's not the modified df
        processed_behavioral_df = BehavioralUtilities.add_winstay_loseshift_loseomit(
            processed_behavioral_df
        )
        # Add post-hoc processing
        processed_behavioral_df = BehavioralUtilities.shift_col_values(
            processed_behavioral_df
        )

        processed_behavioral_df = BehavioralUtilities.interpolate_block(
            processed_behavioral_df, trails_in_block=30
        )
        print("here")
        processed_behavioral_df = BehavioralUtilities.del_first_row(
            processed_behavioral_df
        )
        # print(processed_behavioral_df.to_string())
        BehavioralUtilities.verify_table(processed_behavioral_df)
        new_path = curr_session.replace(".csv", "_ABET_processed.csv")
        processed_behavioral_df.to_csv(
            new_path,
            index=True,
        )
    except:
        print("AN ERROR OCURRED!")
        pass


ROOT_SESSION = r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1/2021-05-18-10-26-03_video_BLA-Insc-6_RDT_D1/BLA-INSC-6 05182021.csv"
# main2(ROOT_SESSION)
