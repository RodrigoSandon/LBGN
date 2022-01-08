import pandas as pd
from scipy import stats
from NeuronSessionTestManager import NeuronSessionTestManager
import sqlite3

from scipy.ndimage import gaussian_filter1d
from matplotlib import pyplot as plt


class Utilities:
    def change_cell_names(df):

        for col in df.columns:

            df = df.rename(columns={col: col.replace("BLA-Insc-", "")})
            # print(col)

        return df

    def zscore(obs_value, mu, sigma):
        return (obs_value - mu) / sigma

    def convert_secs_to_idx(
        unknown_time_min, unknown_time_max, reference_pair: dict, hertz: int
    ):
        reference_time = list(reference_pair.keys())[0]  # has to come from 0
        reference_idx = list(reference_pair.values())[0]

        idx_start = (unknown_time_min * hertz) + reference_idx

        idx_end = (unknown_time_max * hertz) + reference_idx  # exclusive
        return int(idx_start), int(idx_end)

    def create_subwindow_for_col(
        df, col, unknown_time_min, unknown_time_max, reference_pair, hertz
    ) -> list:
        idx_start, idx_end = Utilities.convert_secs_to_idx(
            unknown_time_min, unknown_time_max, reference_pair, hertz
        )
        subwindow = df[col][idx_start:idx_end]
        return subwindow

    def create_subwindow_of_list(
        lst, unknown_time_min, unknown_time_max, reference_pair, hertz
    ) -> list:
        idx_start, idx_end = Utilities.convert_secs_to_idx(
            unknown_time_min, unknown_time_max, reference_pair, hertz
        )

        subwindow_lst = lst[idx_start:idx_end]
        return subwindow_lst

    def zscore(obs_value, mu, sigma):
        return (obs_value - mu) / sigma

    def custom_standardize(
        df, unknown_time_min, unknown_time_max, reference_pair: dict, hertz: int
    ):
        for col in df.columns:
            subwindow = Utilities.create_subwindow_for_col(
                df, col, unknown_time_min, unknown_time_max, reference_pair, hertz
            )
            mean_for_cell = stats.tmean(subwindow)
            stdev_for_cell = stats.tstd(subwindow)

            new_col_vals = []
            for ele in list(df[col]):
                z_value = Utilities.zscore(ele, mean_for_cell, stdev_for_cell)
                new_col_vals.append(z_value)

            df[col] = new_col_vals
        return df

    def gaussian_smooth(df, sigma: float = 1.5):
        # so that it applys smoothing within a cell and not across cells
        df = df.T.apply(gaussian_filter1d, sigma=sigma, axis=0)
        # switch back to og transformation
        return df.T

    def pie_chart(
        csv_path: str, test_name: str, data: list, labels: list, replace_name: str
    ):
        fig = plt.figure(figsize=(10, 7))
        plt.pie(data, labels=labels, autopct="%1.2f%%")
        plt.title(test_name)
        new_name = csv_path.replace(".csv", replace_name)
        plt.savefig(new_name)
        plt.close()

    def make_replace_name_suffix_prefix(standardize: bool, smooth: bool):
        return f"_norm-{standardize}_smooth-{smooth}"


class IdentityTest(Utilities):
    def __init__(
        self,
        db_name: str,
        csv_path: str,
        session: str,
        event_type: str,
        df: pd.DataFrame,
        cursor,
        standardize: bool,
        smooth: bool,
        lower_bound_time: int,
        upper_bound_time: int,
        reference_pair: dict,
        hertz: int,
        test: str,
    ):

        super().__init__()

        self.db_name = db_name
        self.csv_path = csv_path
        self.session = session
        self.event_type = event_type
        self.cursor = cursor
        self.test = test
        self.table_name = session

        self.standardize = standardize
        self.smooth = smooth
        self.lower_bound_time = lower_bound_time
        self.upper_bound_time = upper_bound_time
        self.reference_pair = reference_pair
        self.hertz = hertz

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

        if test == "ranksum":
            IdentityTest.wilcoxon_rank_sum(self)

        else:
            print("Test is not available!")

        def make_col_name(analysis, sample_size, subwindow_base, subwindow_post):
            key_name = "_".join(
                analysis,
                event_type,
                sample_size,
                subwindow_base,
                subwindow_post,
                standardize,
                smooth,
            )

            return key_name

        # does per cell, but df needs to be loaded
        def wilcoxon_rank_sum(number_cells, cell):

            sub_df_baseline_lst = Utilities.create_subwindow_of_list(
                list(self.df[cell]),
                unknown_time_min=-10,
                unknown_time_max=0,
                reference_pair={0: 100},
                hertz=10,
            )

            sub_df_lst = Utilities.create_subwindow_of_list(
                list(self.df[cell]),
                unknown_time_min=0,
                unknown_time_max=2,
                reference_pair={0: 100},
                hertz=10,
            )

            result_greater = stats.ranksums(
                sub_df_lst, sub_df_baseline_lst, alternative="greater"
            )

            result_less = stats.ranksums(
                sub_df_lst, sub_df_baseline_lst, alternative="less"
            )

            id = None
            if result_greater.pvalue < (0.01 / number_cells):
                id = "+"
            elif result_less.pvalue < (0.01 / number_cells):
                id = "-"
            else:
                id = "Neutral"

            return id

        def give_identity(self):
            number_cells = len(list(self.df.columns))

            for cell in list(self.df.columns):
                neuron = NeuronSessionTestManager(cell)

                # check if cell already exists, (not iin first run)
                result = None
                for row in cursor.execute(f"SELECT * FROM {self.db_name} WHERE neurons.cell_name = (?)", (cell,)):
                    result = row

                #print(f"Result: {result}")
                # cell doesn't exists: means we have an empty table
                new_col_name = make_col_name(self.test,
                                             event_type,
                                             sample_size=number_cells,
                                             subwindow_base="-10-0",
                                             subwindow_post="0-2",
                                             standardize=False,
                                             smooth=False)

                if not isinstance(result, tuple):

                    # insert cell name
                    cursor.execute(
                        f"INSERT INTO {self.db_name} VALUES (?)", (cell,))
                    # then add test (new col)
                    cursor.execute(
                        f"ALTER TABLE {self.table_name} ADD (?) TEXT", (new_col_name,))

                    # then add it's id value
                    id = wilcoxon_rank_sum(number_cells, cell)

                    # should still work since still in the same cell
                    cursor.execute(
                        f"INSERT INTO {self.db_name} ({new_col_name}) VALUES (?)", (id,))

                # if already exists: dont insert cell name, jus add test (new col) and its id val, must be a new subevent
                # (some data already exists in the db from first run)
                else:
                    # now new to indicate where to put new value exactly

                    cursor.execute(
                        f"ALTER TABLE {self.table_name} ADD (?) TEXT", (new_col_name,))

                    id = wilcoxon_rank_sum(number_cells, cell)

                    cursor.execute(
                        f"UPDATE {self.db_name} SET {new_col_name}=(?) WHERE cell_name= (?)", (id, cell))


def main():

    # Set db name and curr subevent path
    db_name = "BLA_Cells_Identity_Tracker"
    CONCAT_CELLS_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData/RDT D2/Shock Ocurred_Choice Time (s)/True/all_concat_cells.csv"

    # Create db connection
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()

    # Create SQl table here
    session = CONCAT_CELLS_PATH.split("/")[6]
    c.execute(f"CREATE TABLE {session} (cell_name TEXT,)")

    # Run a test on a subevent
    IdentityTest(
        db_name,
        CONCAT_CELLS_PATH,
        session,
        event_type="_".join(
            CONCAT_CELLS_PATH.split("/")[7], CONCAT_CELLS_PATH.split("/")[8]),
        df=Utilities.change_cell_names(pd.read_csv(CONCAT_CELLS_PATH)),
        cursor=c,
        standardize=False,
        smooth=False,
        lower_bound_time=0,
        upper_bound_time=2,
        reference_pair={0: 100},
        hertz=10,
        test="ranksum",
    )
    conn.commit()

    rows = c.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
