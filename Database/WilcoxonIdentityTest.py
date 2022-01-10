import pandas as pd
from scipy import stats
from NeuronSessionTestManager import NeuronSessionTestManager
import sqlite3
import glob, os

from scipy.ndimage import gaussian_filter1d
from matplotlib import pyplot as plt


class Utilities:
    def find_paths_startswith(root_path, startswith) -> list:

        files = glob.glob(
            os.path.join(root_path, "**", "%s*") % (startswith),
            recursive=True,
        )

        return files

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


class WilcoxonIdentityTest:
    def __init__(
        self,
        conn,
        db_name: str,
        csv_path: str,
        session: str,
        event_type: str,
        df: pd.DataFrame,
        cursor,
        standardize: bool,
        smooth: bool,
        base_lower_bound_time: int,
        base_upper_bound_time: int,
        lower_bound_time: int,
        upper_bound_time: int,
        reference_pair_s: int,
        reference_pair_idx: int,
        reference_pair: dict,
        hertz: int,
        test: str,
    ):

        self.conn = conn
        self.db_name = db_name
        self.csv_path = csv_path
        self.session = session
        self.event_type = event_type
        self.cursor = cursor
        self.test = test
        self.table_name = session

        self.standardize = standardize
        self.smooth = smooth
        self.base_lower_bound_time = base_lower_bound_time
        self.base_upper_bound_time = base_upper_bound_time
        self.lower_bound_time = lower_bound_time
        self.upper_bound_time = upper_bound_time

        self.reference_pair_s = reference_pair_s
        self.reference_pair_idx = reference_pair_idx
        self.reference_pair = reference_pair
        self.hertz = hertz

        if test == "ranksum":
            self.give_identity_wilcoxon()

        else:
            print("Test is not available!")

    def make_col_name(self, sample_size, subwindow_base, subwindow_post):

        self.event_type = self.event_type.replace(" ", "_")
        lst = [
            self.test,
            self.event_type,
            str(sample_size),
            subwindow_base,
            subwindow_post,
            str(self.standardize),
            str(self.smooth),
        ]
        # SQL DOESNT LIKE THESE CHARACTERS
        key_name = "_".join(lst)
        if "." in key_name:
            key_name = key_name.replace(".", "dot")
        if "(" in key_name:
            key_name = key_name.replace("(", "")
        if ")" in key_name:
            key_name = key_name.replace(")", "")
        if "," in key_name:
            key_name = key_name.replace(",", "")
        if "'" in key_name:
            key_name = key_name.replace("'", "")
        return key_name

    def wilcoxon_rank_sum(self, number_cells, cell):

        sub_df_baseline_lst = Utilities.create_subwindow_of_list(
            list(self.df[cell]),
            unknown_time_min=self.base_lower_bound_time,
            unknown_time_max=self.base_upper_bound_time,
            reference_pair={0: 100},
            hertz=10,
        )

        sub_df_lst = Utilities.create_subwindow_of_list(
            list(self.df[cell]),
            unknown_time_min=self.lower_bound_time,
            unknown_time_max=self.upper_bound_time,
            reference_pair={0: 100},
            hertz=10,
        )

        result_greater = stats.mannwhitneyu(
            sub_df_lst, sub_df_baseline_lst, alternative="greater"
        )

        result_less = stats.mannwhitneyu(
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

    def give_identity_wilcoxon(self):
        number_cells = len(list(self.df.columns))

        new_col_name = self.make_col_name(
            number_cells, subwindow_base="minus10_to_0", subwindow_post="0_to_2"
        )
        # add test, comes before all the identity giving to cells
        print(new_col_name)
        self.cursor.execute(
            f"ALTER TABLE {self.table_name} ADD COLUMN {new_col_name} TEXT"
        )
        self.conn.commit()

        for cell in list(self.df.columns):

            # check if cell already exists, (not iin first run)
            result = None
            for row in self.cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE {self.table_name}.cell_name = ?",
                (cell,),
            ):
                result = row

            # then add it's id value
            id = self.wilcoxon_rank_sum(number_cells, cell)
            # print(id)

            # cell doesn't exists: means we have an empty table
            if not isinstance(result, tuple):

                # insert cell name and id
                self.cursor.execute(
                    f"INSERT INTO {self.table_name} VALUES (?,?)", [cell, id]
                )
                self.conn.commit()

            # if cellalready exists: dont insert cell name, jus add test (new col) and its id val, must be a new subevent
            # (some data already exists in the db from first run)
            else:
                # now new to indicate where to put new value exactly

                self.cursor.execute(
                    f"UPDATE {self.table_name} SET {new_col_name}=(?) WHERE {self.table_name}.cell_name= (?)",
                    [id, cell],
                )
                self.conn.commit()


def main():
    ROOT = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData"

    # Set db name and curr subevent path
    db_name = "BLA_Cells_Ranksum_Post_Activity"

    # Create db connection
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()

    for session in os.listdir(ROOT):
        print(session)
        SESSION_PATH = os.path.join(ROOT, session)

        csvs = Utilities.find_paths_startswith(SESSION_PATH, "all_concat_cells.csv")

        # Create SQl table here
        table_name = session.replace(" ", "_")
        c.execute(
            f"""

        CREATE TABLE {table_name} (
            cell_name TEXT
        )
        
        """
        )

        # IF table already created?

        for csv in csvs:
            CONCAT_CELLS_PATH = csv

            list_of_eventtype_name = [
                CONCAT_CELLS_PATH.split("/")[7],
                CONCAT_CELLS_PATH.split("/")[8],
            ]

            # Run a test on a subevent
            WilcoxonIdentityTest(
                conn,
                db_name,
                CONCAT_CELLS_PATH,
                session="RDT_D2",
                event_type="_".join(list_of_eventtype_name),
                df=Utilities.change_cell_names(pd.read_csv(CONCAT_CELLS_PATH)),
                cursor=c,
                standardize=False,
                smooth=False,
                base_lower_bound_time=0,
                base_upper_bound_time=-10,
                lower_bound_time=0,
                upper_bound_time=2,
                reference_pair={0: 100},
                hertz=10,
                test="ranksum",
            )


if __name__ == "__main__":
    main()
