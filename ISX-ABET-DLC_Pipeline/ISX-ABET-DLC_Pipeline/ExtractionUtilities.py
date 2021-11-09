from preprocess import preprocess
from pathlib import Path
from typing import List
import os, glob


class ExtractionUtilities:
    def preprocess_single_vid():
        filename = input("What is the path to the raw '.isxd' file? ")
        preprocess(Path(filename))

    def preprocess_multiple_vids(root_path):
        def find_video_paths(root_directory: Path) -> List[Path]:

            vids = []
            numberISXDFiles = 0

            for root, dirs, files in os.walk(root_directory):
                # print(root)
                for name in files:
                    if name.endswith(".isxd"):
                        numberISXDFiles += 1
                        file = os.path.join(root, name)
                        vids.append(file)
            print("number of files: ", numberISXDFiles)
            # print(*vids, sep="\n")
            vids  # reverse just to try to get a less huge file on first iter
            return vids

        dir_for_processed_vids = Path(r"/media/rory/RDT VIDS/PTP_Inscopix_#3")

        def vids_to_process(dir: Path) -> List[Path]:

            vids_left_to_process = []

            for root, dirs, files in os.walk(dir):
                # print(dirs)
                for i in dirs:
                    # print(os.listdir(os.path.join(root, i)))
                    if (len(os.listdir(os.path.join(root, i))) < 6) and i.startswith(
                        "Session"
                    ):  # less than 6 means the isx file didnt fully process yet
                        vids_left_to_process.append(i)

            # print(*vids_left_to_process, sep="\n")
            # print(len(vids_left_to_process))

            return vids_left_to_process

        def generate_output_dir(input_video_path: Path) -> Path:
            """Given a video to be preprocessed, returns a directory where all of the preprocessed files will be saved

            Args:
                input_video_path (Path): Path to raw .isxd file

            Returns:
                Path: Path to directory where all preprocessed files will be saved
            """
            # change this to alter the location of the preprocessed files
            # example: /media/rory/PTP Inscopix 1/Inscopix/Raw Inscopix Data Files/BLA-Insc-3/Good Sessions/Session-20210216-173241-BLA-Insc-3/2021-02-16-17-39-50_video.isxd
            # /media/rory/PTP Inscopix 3/Inscopix_to_Analyze/BLA-Insc-5/Session-20210510-093930_BLA-Insc-5_RM_D1/2021-05-10-09-45-37_video_BLA-Insc-5_RM_D1.isxd
            name_folder = input_video_path.split("/")[5]
            name_session = input_video_path.split("/")[6]
            name_file = input_video_path.split("/")[7].replace(".isxd", "")
            outdir = Path(
                "/media/rory/RDT VIDS/PTP_Inscopix_#3/%s/%s/%s"
                % (name_folder, name_session, name_file)
            )
            outdir.mkdir(exist_ok=True, parents=True)
            return outdir
