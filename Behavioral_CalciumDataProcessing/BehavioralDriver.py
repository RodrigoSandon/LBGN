import pandas as pd
import numpy as np
from BehavioralSession import BehavioralSession
from BehavioralUtilities import BehavioralUtilities


class BehavioralDriver:
    def main():
        ABET_1 = BehavioralSession(
            "BLA-INSC-6 05182021",
            "/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1/2021-05-18-10-26-03_video_BLA-Insc-6_RDT_D1/BLA-INSC-6 05182021.csv",
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
        processed_behavioral_df = BehavioralUtilities.del_first_row(
            processed_behavioral_df
        )
        # print(processed_behavioral_df.to_string())
        BehavioralUtilities.verify_table(processed_behavioral_df)
        processed_behavioral_df.to_csv(
            "/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#3/BLA-Insc-6/Session-20210518-102215_BLA-Insc-6_RDT_D1/2021-05-18-10-26-03_video_BLA-Insc-6_RDT_D1/BLA-INSC-6 05182021_ABET_processed_fixed111021.csv",
            index=True,
        )


if __name__ == "__main__":
    BehavioralDriver.main()
