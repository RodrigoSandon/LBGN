import sqlite3
import matplotlib
import pandas as pd
import copy
import os

import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn3_circles

from pprint import pprint as pp
import circlify as circ


"""
Assumptions:

1. You'll get results from both post/pre activity databases.
"""


class StreamProportions:
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

        self.stream_responsiveness()
        self.stream_activity()

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
                "nonresp_cells": [],
            }

            for row_idx in range(len(self.df)):
                # pull the cell_name
                cell_name = self.df.iloc[row_idx]["cell_name"]
                # pull the id for the subevent
                id = self.df.iloc[row_idx][full_subevent_name]
                # insert to according list
                if id == "Neutral":
                    d_activity[full_subevent_name]["N_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["nonresp_cells"].append(
                        cell_name
                    )
                elif id == "+":
                    d_activity[full_subevent_name]["+_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["resp_cells"].append(cell_name)
                else:
                    d_activity[full_subevent_name]["-_cells"].append(cell_name)
                    d_responsiveness[full_subevent_name]["resp_cells"].append(cell_name)

        return d_activity, d_responsiveness

    def stacked_barplot(self):
        pass

    def find_subcategories_within_list(
        self, mylist: list, resp_list: list, nonresp_list: list
    ) -> list:
        new_resp_list = []
        new_nonresp_list = []

        for i in mylist:
            if i in resp_list:
                new_resp_list.append(i)
            else:
                new_nonresp_list.append(i)
            """elif i in nonresp_list:
                new_nonresp_list.append(i)"""

        print("mylist:", len(mylist))
        # print("new_resp:", new_resp_list)
        # print("new_nonresp:", new_nonresp_list)

        return [len(new_resp_list), len(new_nonresp_list)]

    def remaining(
        self, mylist: list, nonresp_list: list,
    ) -> list:  # should only include resp, so eliminate all nonresp cells
        cop_my_list = copy.deepcopy(mylist)

        """for i in cop_resp_list:
            if i not in mylist:
                cop_resp_list.remove(i)"""

        for i in cop_my_list:
            if i in nonresp_list:
                cop_my_list.remove(i)

        return cop_my_list

    def stream_responsiveness(self):
        cell_ids_activity, cell_ids_responsiveness = self.create_venndiagram_dict()

        # OVERALL PROPORTION CHANGE ALONG SUBEVENTS
        labels = []
        resp_count = []
        nonresp_count = []

        # TRACKING ONLY RESP CELLS ALONG SUBEVENTS
        # subevent_name : [Resp, non-resp #]
        # subevent_name_subevent_name : [Resp, non-resp #]
        # subevent_name_subevent_name_subevent_name : [Resp, non-resp #]
        curr_resp = None
        tracking_resp = {}

        # TRACKING ONLY NON-RESP????

        for count, subevent in enumerate(cell_ids_responsiveness):
            subevent_short = subevent.split("_")[1]
            if count == 0:
                labels.append(subevent_short)
                tracking_resp[subevent_short] = []
            else:
                labels.append(labels[count - 1] + "_" + subevent_short)

            # OVERALL PROPORTION
            resp_count.append(len(cell_ids_responsiveness[subevent]["resp_cells"]))
            nonresp_count.append(
                len(cell_ids_responsiveness[subevent]["nonresp_cells"])
            )
            # TRACKING RESP
            if count == 0:
                curr_resp = cell_ids_responsiveness[subevent]["resp_cells"]
                tracking_resp[subevent_short].append(
                    len(cell_ids_responsiveness[subevent]["resp_cells"])
                )
                tracking_resp[subevent_short].append(
                    len(cell_ids_responsiveness[subevent]["nonresp_cells"])
                )

            else:

                # We have a list of previous resp cells already, which of these are now resp.nonresp?
                # return new proportion here
                tracking_resp[
                    labels[count - 1] + "_" + subevent_short
                ] = self.find_subcategories_within_list(
                    curr_resp,
                    cell_ids_responsiveness[subevent]["resp_cells"],
                    cell_ids_responsiveness[subevent]["nonresp_cells"],
                )

                # update curr_resp, bc one has existed already
                # grabbing curr's subevent resp cells based on previous resp cells
                curr_resp = self.remaining(
                    curr_resp, cell_ids_responsiveness[subevent]["nonresp_cells"]
                )

            # print("CURR RESP:", len(curr_resp))
            print("Labels:", labels)
            print("Resp count:", resp_count)
            print("Non-resp count:", nonresp_count)
            print("TRACKING RESP")
            print(tracking_resp)

        # now that cells are categorized, start chaining

    def stream_activity(self):
        cell_ids_activity, cell_ids_responsiveness = self.create_venndiagram_dict()

        # subevent name : [+,-, neutral proportion]
        venn_diagrams = {}

        for subevent in cell_ids_responsiveness:
            # for each subevent (first one being or base case)
            # each subevent will create a data structure that's ready for venn diagram
            pass

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

            StreamProportions(
                session_df, c, db, session, analysis, "Choice_Time", subevent_chain,
            )
            break
        conn.close()
        break


if __name__ == "__main__":
    main()
