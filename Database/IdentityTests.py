from Behavioral_Calcium_DLC_Analysis.Methods.cell_classification import Utilities
import pandas as pd
from scipy.stats import stats
from Neuron import Neuron
import sqlite3


class IdentityTest(Utilities):
    def __init__(
        self,
        csv_path: str,
        session: str,
        event_type: str,
        df: pd.DataFrame,
        standardize: bool,
        smooth: bool,
        lower_bound_time: int,
        upper_bound_time: int,
        reference_pair: dict,
        hertz: int,
        test: str,
    ):

        super().__init__()

        self.csv_path = csv_path
        self.session = session
        self.event_type = event_type
        self.standardize = standardize
        self.smooth = smooth
        # for the time window we are doing the tests based off of
        self.lower_bound_time = lower_bound_time
        # for the time window we are doing the tests based off of
        self.upper_bound_time = upper_bound_time
        # to know how to convert secs to idx, should be 0:100, 100 to account for exclusivity at end
        # so if 0:100, then it's interpreted as 0:99
        self.reference_pair = reference_pair
        self.hertz = hertz  # helps in calculating conversion

        if standardize == True and smooth == True:  # major
            self.df = Utilities.custom_standardize(
                df, lower_bound_time, upper_bound_time, reference_pair, hertz
            )
            self.df = Utilities.gaussian_smooth(self.df)
        elif standardize == False and smooth == False:  # major
            self.df = df
        elif standardize == True and smooth == False:
            self.df = Utilities.custom_standardize(
                df, lower_bound_time, upper_bound_time, reference_pair, hertz
            )
        elif standardize == False and smooth == True:
            self.df = Utilities.gaussian_smooth(df)

        if test == "stdev binary test":
            IdentityTest.stdev_difference_test(self)
            IdentityTest.stdev_difference_test_shuffled(self)
        elif test == "two sample t test":
            IdentityTest.two_sample_t_test(self)
        elif test == "one sample t test":
            IdentityTest.one_sample_t_test(self)
        elif test == "wilcoxon rank sum test":
            IdentityTest.wilcoxon_rank_sum(self)
        elif test == "all":
            IdentityTest.stdev_difference_test(self)
            IdentityTest.stdev_difference_test_shuffled(self)
            IdentityTest.two_sample_t_test(self)
            IdentityTest.one_sample_t_test(self)
            IdentityTest.wilcoxon_rank_sum(self)

        else:
            print("Test is not available!")

        def wilcoxon_rank_sum(self):  # wilcoxon rank sum test
            active_cells = []
            inactive_cells = []
            neutral_cells = []
            number_cells = len(list(self.df.columns))

            for col in list(self.df.columns):  # a col is a cell
                # Check if neuron's cell name already exists in this current session's table
                neuron = Neuron(col)

                # neuron's will never match by their object id, instead, by their attribute (cell name)

                sub_df_baseline_lst = Utilities.create_subwindow_of_list(
                    list(self.df[col]),
                    unknown_time_min=-10,
                    unknown_time_max=0,
                    reference_pair={0: 100},
                    hertz=10,
                )

                sub_df_lst = Utilities.create_subwindow_of_list(
                    list(self.df[col]),
                    unknown_time_min=0,
                    unknown_time_max=2,
                    reference_pair={0: 100},
                    hertz=10,
                )

                result_greater = stats.mannwhitneyu(
                    sub_df_lst, sub_df_baseline_lst, alternative="greater"
                )

                result_less = stats.mannwhitneyu(
                    sub_df_lst, sub_df_baseline_lst, alternative="less"
                )

                # 0.005 * 2 = 0.01
                if result_greater.pvalue < (0.01 / number_cells):
                    neuron.add_id(
                        self.session,
                        self.test,
                        sample_size=number_cells,
                        subwindow_base="-10-0",
                        subwindow_post="0-2",
                        standardize=False,
                        smooth=False,
                        identity="+",
                    )
                elif result_less.pvalue < (0.01 / number_cells):
                    neuron.add_id(
                        self.session,
                        self.test,
                        sample_size=number_cells,
                        subwindow_base="-10-0",
                        subwindow_post="0-2",
                        standardize=False,
                        smooth=False,
                        identity="-",
                    )
                else:
                    neuron.add_id(
                        self.session,
                        self.test,
                        sample_size=number_cells,
                        subwindow_base="-10-0",
                        subwindow_post="0-2",
                        standardize=False,
                        smooth=False,
                        identity="Neutral",
                    )

            d = {
                "(+) Active Cells": len(active_cells),
                "(-) Active Cells": len(inactive_cells),
                "Neutral Cells": len(neutral_cells),
            }

            replace_name_prefix = Utilities.make_replace_name_suffix_prefix(
                self.standardize, self.smooth
            )


def main():

    # Create SQl table here
    conn = sqlite3.connect("BLA_Cells_Identity_Tracker.db")
    c = conn.cursor()

    CONCAT_CELLS_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData/RDT D2/Shock Ocurred_Choice Time (s)/True/all_concat_cells.csv"

    session = CONCAT_CELLS_PATH.split("/")[6]

    c.execute(
        f"""

    CREATE TABLE {session} (
        
        cell_name TEXT,
        cell_object BLOB
    )   
    """
    )

    event_type = "_".join(
        CONCAT_CELLS_PATH.split("/")[7], CONCAT_CELLS_PATH.split("/")[8]
    )
    df = pd.read_csv(CONCAT_CELLS_PATH)
    df = Utilities.change_cell_names(df)

    IdentityTest(
        CONCAT_CELLS_PATH,
        session,
        event_type,
        df,
        standardize=False,
        smooth=False,
        lower_bound_time=0,
        upper_bound_time=2,
        reference_pair={0: 100},
        hertz=10,
        test="wilcoxon rank sum test",
    )


if __name__ == "__main__":
    main()
