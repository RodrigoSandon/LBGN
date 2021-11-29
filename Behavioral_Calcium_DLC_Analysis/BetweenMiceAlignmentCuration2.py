import os, glob
import pandas as pd
import numpy as np


def find_csv_files(root_path, endswith):

    files = glob.glob(
        os.path.join(root_path, "**", "*%s") % (endswith),
        recursive=True,
    )

    return files


def truncate_csvs_in_root(root_path, name_of_files_to_trunc, len_threshold):

    files_to_truncate = find_csv_files(root_path, name_of_files_to_trunc)

    df_database = TableDatabase()

    for file in files_to_truncate:
        table = Table(file, len_threshold)
        table.include_table(drop_row=False)

    print(f"Number of jagged tables before: {df_database._number_of_jagged_dfs}")

    df_database._number_of_jagged_dfs = 0
    df_database._jagged_dfs = []

    for file in files_to_truncate:
        table = Table(file, len_threshold)
        table.include_table(drop_row=True)
    print(f"Number of jagged tables after: {df_database._number_of_jagged_dfs}")


class TableDatabase(object):
    """Don't want to store all this data in one object, rather, just want to update
    its parameters that are is is meta of tables."""

    _number_of_jagged_dfs = 0
    _jagged_dfs = []


class Table(TableDatabase):
    def __init__(self, df_path, len_threshold):
        # super().__init__()
        self.path = df_path
        self.df = pd.read_csv(df_path)
        self.len_threshold = len_threshold

    def check_if_df_len_equals_thres(self):
        equals_threshold = True
        for col in self.df.columns:
            for count, val in enumerate(list(self.df[col])):
                if str(val) == "nan":
                    # print(f"Column {col} in {self.path} has NaN at row {count}.")
                    equals_threshold = False

        return equals_threshold

    def drop_last_row_df(self):
        self.df = self.df.drop(self.df.tail(1).index)

    def include_table(self, drop_row: bool):
        equals_threshold = self.check_if_df_len_equals_thres()
        if drop_row == True:  # indicates whether we want to acc drop rows yet
            if equals_threshold is True:  # don't do anything if the df is not jagged
                pass
            elif equals_threshold is False:  # if it is jagged, do everything
                self.drop_last_row_df()
                TableDatabase._number_of_jagged_dfs += 1
                TableDatabase._jagged_dfs.append(self.path)
                self.save_table()

        elif drop_row == False:
            if equals_threshold is True:  # don't do anything if the df is not jagged
                pass
            elif (
                equals_threshold is False
            ):  # if it is jagged, do everything except dropping
                TableDatabase._number_of_jagged_dfs += 1
                TableDatabase._jagged_dfs.append(self.path)

    def save_table(self):
        new_path = self.path.replace(".csv", "_truncated.csv")
        self.df.to_csv(new_path, index=False)


def main():
    ROOT_PATH = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData"

    truncate_csvs_in_root(
        ROOT_PATH, name_of_files_to_trunc="all_concat_cells.csv", len_threshold=200
    )


main()
