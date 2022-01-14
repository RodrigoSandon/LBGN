import sqlite3
import pandas as pd
import os

"""
Assumptions:

1. You'll get results from both post/pre activity databases.
"""


class StreamVennDiagrams:
    def __init__(
        self,
        df: pd.DataFrame,
        c,
        db: str,
        session: str,
        analysis: str,
        start_choice_collect: str,
        subevent_chain: list,
    ):
        self.df = df
        self.c = c
        self.db = db
        self.session = session
        self.analysis = analysis
        self.start_choice_collect = start_choice_collect
        self.subevent_chain = subevent_chain

        self.d_to_venns = self.stream()

    def make_substr_of_col_name(self, param: str):

        if " " in param:
            param = param.replace(" ", "_")

        col_name_substr = f"{self.analysis}_{param}_{self.start_choice_collect}"

        return col_name_substr

    def create_venndiagram_dict(self):
        d_activity = {}
        """
        d_activity = {
            subevent : {
                +_cells : [cell_name, ...],
                         .
                         .
                         .
            },
            subevent : {
                -_cells : [cell_name, ...],
                         .
                         .
                         .
            },
            subevent : {
                N_cells : [cell_name, ...],
                         .
                         .
                         .
            },
        }
        """
        d_responsiveness = {}
        """
        d_responsiveness = {
            subevent : {
                resp_cells : [cell_name, ...],
                         .
                         .
                         .
            },
            subevent : {
                N_cells : [cell_name, ...],
                         .
                         .
                         .
            },
        }
        """

        for param in self.subevent_chain:  # param = a subevent
            # make the colname that your going to look for for this
            subevent_substr = self.make_substr_of_col_name(param)
            # now search it in the df, get the full name of col
            full_subevent_name = None
            for col in list(self.df.columns):
                if subevent_substr in col:
                    full_subevent_name = col
            # have subevent name
            # pull the cell_name col values
            # now have full col name, now i can id values for this subevent
            d_activity[full_subevent_name] = {
                "+_cells": [],
                "-_cells": [],
                "N_cells": [],
            }

            d_responsiveness[full_subevent_name] = {
                "resp_cells": [],
                "N_cells": [],
            }

            for row_idx in range(len(self.df)):
                # pull the cell_name
                cell_name = self.df.iloc[row_idx]["cell_name"]
                # pull the id for the subevent
                id = self.df.iloc[row_idx][full_subevent_name]
                # insert to according list
                if id == "Neutral":
                    d_activity[full_subevent_name]["N_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["N_cells"].append(cell_name)
                elif id == "+":
                    d_activity[full_subevent_name]["+_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["resp_cells"].append(cell_name)
                else:
                    d_activity[full_subevent_name]["-_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["resp_cells"].append(cell_name)

        return d_activity, d_responsiveness

    def venn_diagram(self):
        pass

    def stream(self):
        cell_ids_activity, cell_ids_responsiveness = self.create_venndiagram_dict()

        # now that cells are categorized, start chaining


def main():
    # select dir where db's exist
    os.chdir("/home/rory/Rodrigo/Database")
    # Following parameters determines how many results we acquire from the same data
    dbs = ["BLA_Cells_Ranksum_Pre_Activity", "BLA_Cells_Ranksum_Post_Activity"]
    session_types = ["RDT_D1", "RDT_D2"]
    analysis = "mannwhitneyu"

    # this is where you customize when chain of events to partake in
    # selecting specific columns to start off with, then each subsequent one wil be pulling
    # Block_Reward_Size_Shock_Ocurred_Choice_Time
    subevent_chain = ["Shock Ocurred", "Reward Size", "Block"]

    for db in dbs:
        print(f"Curr db: {db}")
        conn = sqlite3.connect(f"{db}.db")
        c = conn.cursor()

        for session in session_types:
            print(f"Curr session: {session}")
            sql_query = pd.read_sql_query(f"SELECT * FROM {session}", conn)
            session_df = pd.DataFrame(sql_query)

            StreamVennDiagrams(
                session_df,
                c,
                db,
                session,
                analysis,
                "Choice_Time",
                subevent_chain,
            )
        conn.close()


if __name__ == "__main__":
    main()
