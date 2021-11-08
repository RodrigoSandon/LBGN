import pandas as pd
import numpy as np
from BehavioralSession import BehavioralSession
from BehavioralUtilities import BehavioralUtilities


class BehavioralDriver:
    def main():
        ABET_1 = BehavioralSession(
            "BLA-INSC-6 06082021",
            "/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6/Session-20210608-095359_BLA-Insc-6_RDT_D3_NEW_SCOPE/2021-06-08-09-54-49_video_BLA-Insc-6_RDT_D3_NEW_SCOPE/BLA-INSC-6 06082021.csv",
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
        print(processed_behavioral_df.to_string())
        BehavioralUtilities.verify_table(processed_behavioral_df)
        processed_behavioral_df.to_csv(
            "/media/rory/PTP Inscopix 2/PTP_Inscopix_#3/BLA-Insc-6/Session-20210608-095359_BLA-Insc-6_RDT_D3_NEW_SCOPE/2021-06-08-09-54-49_video_BLA-Insc-6_RDT_D3_NEW_SCOPE/BLA-INSC-6 06082021_ABET_processed.csv",
            index=True,
        )


if __name__ == "__main__":
    BehavioralDriver.main()
