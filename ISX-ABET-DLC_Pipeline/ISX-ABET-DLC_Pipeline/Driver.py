from ExtractionUtilities import ExtractionUtilities
from typing import List


class Driver:
    def preprocess_single_or_multiple_vids(
        one: str, multiple: str
    ) -> ExtractionUtilities:
        number_to_preprocess = input(
            "Would you you like to preprocess one vid or multiple vids? "
        )

        if one in number_to_preprocess:
            ExtractionUtilities.preprocess_single_vid()
        elif multiple in number_to_preprocess:
            input_1 = input(
                "Would you like to specify a list of paths or an entire root directory?"
            )
            if "list" in input_1:

            Driver.preprocess_multiple_vids
        else:
            print("Please choose a valid option!")
            print("Your input must either contain %s or %s." % (one, multiple))
    
    def preprocess_multiple_vids():
        print(
            "Giving a list only preprocesses the according .isxd files. While providing a path makes it so that the program finds all .isxd files recursively."
        )
        paths_to_provide = input("Give a list or mouse path: ")
        if isinstance(paths_to_provide, List):
            print(paths_to_provide)
        elif isinstance(paths_to_provide, str):
            ExtractionUtilities.preprocess_multiple_vids(paths_to_provide)

    def main():

        Driver.preprocess_single_or_multiple_vids("one", "multiple")
        """
        Steps:
        1) preprocess_single_or_multiple_vids:
            - asks the user whether it wants to preprocess one vid or multiple
            - based on the answer, calls the preprocess function
                - 1 VID INPUT: path of raw isxd file via a pop up
                - MULTIPLE VIDS INPUT: path of entire mouse folder, finds ".isxd" files
                recursively

            OUT: downsampled.isxd, spatial_filtered.isxd, motion_corrected.isxd, cnmfe_cellset.isxd
            for the same directory the raw .isxd file was found in
        """

        """ROOT_DIR = Path(
            r"/media/rory/PTP Inscopix 3/Inscopix_to_Analyze"
        )  # change this path to where your videos are stored
        vids = find_video_paths(ROOT_DIR)
        # print(*vids, sep="\n")
        # print(len(vids))

        vids_left = vids_to_process(dir_for_processed_vids)
        print(vids_left)
        vids_filtered = []

        for vid in vids:
            name_to_locate = vid.split("/")[7]
            if name_to_locate in vids_left:
                vids_filtered.append(vid)

        print("VIDS LEFT:")
        print(*vids_filtered, sep="\n")

        if len(vids_filtered) != 0:
            for i in vids_filtered:
                output_dir = generate_output_dir(i)
                preprocess(in_path=i, out_dir=output_dir)
        else:
            for i in vids:
                print(i)
                output_dir = generate_output_dir(i)
                preprocess(in_path=i, out_dir=output_dir)"""


if __name__ == "__main__":
    Driver.main()
