"""PROGRAM FEATURE 1: Extracting/aligning data by parts (modularity).

When including just root folder path: <- Does all mice, sessions that can match, 
combos that can match, subcombos that can match.

d = {
    Root {
        Mouse 1: {
            Session 1: {
                Combo 1: {
                    Subcombo 1: {
                        concat_cells.csv
                    }
                }
            },
        }
    }
}
        
When including just mice paths: <- Does all sessions, combos, and subcombos that can match 
across X mice.

d = {
    Mouse 1: {
        Session 1: {
            Combo 1: {
                Subcombo 1: {
                    concat_cells.csv
                }
            }
        },
    }
}

When including just sessions paths. <- Does all combos and sub combos for the given sessions
you've indicated (which should be across different mice). A checker will check whether these 
sessions actually match.

d = {
    Session 1: {
        Combo 1: {
            Subcombo 1: {
                concat_cells.csv
            }
        }
    },
}

When including just combo paths <- Does all subcombos for the given combos you've indicated
(which should be across different mice). A checker will check whether the combo's sessions 
and combos themselves match.

d = {
    Combo 1: {
        Subcombo 1: {
            concat_cells.csv
        }
    }
}

When including just subcombo paths <- Does one across-mice-cell concatenation between two similar
events. Program will check whether the subcombo's combo, subcombo's sessions, and combos.

d = {
    Subcombo 1: {
        concat_cells.csv
    }
}

"""

""" PROGRAM FEATURE 2: Extracting/aligning subsets of data for the entire database.

What if you want to apply an entire process for all the information you have avaliable but
only require a subset of info to be extracted from it (instead of having to run everything
to get what you want)?

In this case, add conditionals to limit the data extraction extraction process.

"""

from _typeshed import Self
from typing import List
from pathlib import Path
import re


class BetweenMiceAligment:
    """
    Functionality goes here.
    """

    def __init__(self, align_all: bool, align_all_subset: bool, align_paths: bool):
        self.avaliable_parameters_to_focus = ["mice", "sessions", "combos", "subcombos"]

        if align_all == True and align_all_subset == False and align_paths == False:
            # Run entire database, don't consider any flexibility
            pass

        elif align_all == False and align_all_subset == True and align_paths == False:
            # Run entire database, flexibility on what to acquire

            params = input(
                f"Choose which parameters you care about: {' '.join(self.avaliable_parameters_to_focus)}"
                + "\nType 'done' to indicate your done."
            )

            done = None
            params_to_focus = ()  # order matters, so a tuple
            while done != "done":
                new_input = input()
                params_to_focus.check_and_append(params_to_focus, new_input)

            for i in params_to_focus:
                specified_params = input(f"Which {i} are you focused on?")

        elif align_all == False and align_all_subset == False and align_paths == True:
            # Don't run entire database, align from the level of specificity the user wants
            pass

    def check_if_string_in_list(self, input_str: str) -> bool:
        check = [i for i in self.avaliable_parameters_to_focus if (i == input_str)]
        return bool(check)

    def check_and_append(self, my_lst: List, input_str: str) -> None:
        if BetweenMiceAligment.check_if_string_in_list(input_str) == True:
            my_lst.append(input_str)
        else:
            print(f"{input_str} is not a valid parameter!")

    def check_if_root(self, key):
        if "root" in key:
            return True
        else:
            False

    def set_root_name(self, key, new_name):
        if BetweenMiceAligment.check_if_root(key) == True:
            self.data_hierarchy[new_name]
        else:
            pass

    def create_hierarchy_root(self):
        pass

    def find_mice_paths(self):
        pass

    def perform_big_process(self):
        pass


class Driver:
    """
    Connecting with the OS goes here.
    """

    def main():
        """
        Root that contains mice data (doesn't have to be the direct root).
        """
        ROOT_MICE_PATH = Path(r"/media/rory/Padlock_DT/BLA_Analysis")
        """
        Input the mice you're interested in concatenating session & cells across.
        """
        mice = []

        """
        Input the sessions within each mice that you want to concatenated cells across.
        
        Note: Functionality is made so that you're able to to get multiple session concatenations
        at once.
        """
        sessions = []

        """
        Input the combinations that you care to concatenate cell traces across for each session.
        """
        combos = []
        """
        Create a BetweenMiceAlignment object.
        """
        process_big = BetweenMiceAligment(root=ROOT_MICE_PATH)


class Cleaner:
    """
    Functionality + connection with the OS goes here to delete files related to BetweenMiceAlignment.
    """

    def main():
        pass


if __name__ == "__main__":
    Driver.main()
    # Cleaner.main()

    """def __init__(
        self,
        root_path: str,
        mice: List,
        sessions_tofind: List,
        combos_tofind: List,
        avg_cell_traces_filename,
    ):
        self.root_path = root_path
        self.mice = mice
        self.sessions_tofind = sessions_tofind
        self.combos_tofind = combos_tofind
        self.avg_cell_traces_filename = avg_cell_traces_filename"""

    """def __init__(self, avg_cell_traces_filename, **kwargs):
        #Only sublevel processing argument names you can include.
        allowed_parameters = ["root", "mice", "sessions", "combos", "subcombos"]
        self.avg_cell_traces_filename = avg_cell_traces_filename
        self.data_hierarchy = (
            {}
        )  # Very important, dictates how folder/file structure will be

        for key, val in kwargs.items():
            valid_param = [i for i in allowed_parameters if (i in key)]
            if bool(valid_param) == True:
                self.key = key
                BetweenMiceAligment.set_root_name(key, new_name="BetweenMiceAlignment")
                # ^if not root, skip this making it in dict

        # ^the check that allows parameters to be used"""
