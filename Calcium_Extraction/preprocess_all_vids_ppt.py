from pathlib import Path
import os
from typing import List
from preprocess import preprocess

ROOT_DIR = Path(r"/media/rory/Nathen's Fantom/Inscopix_to_Analyze")
# ^Change this path to where your videos are stored
dir_for_processed_vids = Path(r"/media/rory/Padlock_DT/BLA_Analysis/PTP_Inscopix_#4")
# ^Change this path to where you want preprocessed files stored


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
    # OLD EXAMPLE 9/20/21: /media/rory/PTP Inscopix 1/Inscopix/Raw Inscopix Data Files/BLA-Insc-3/Good Sessions/Session-20210216-173241-BLA-Insc-3/2021-02-16-17-39-50_video.isxd

    # NEW EXAMPLE 11/19/21: /media/rory/Nathen's Fantom/Inscopix_to_Analyze/BLA-Insc-11/PR D1/Session-20211108-113157/2021-11-08-11-34-35_video_green.isxd

    ################### Change this to alter the location of the preprocessed files ###############################
    mouse_name = input_video_path.split("/")[5]
    session_type = input_video_path.split("/")[6]
    session_name = input_video_path.split("/")[7]
    ###################### Change this to alter the location of the preprocessed files ############################
    outdir = Path(
        f"{dir_for_processed_vids}/{mouse_name}/{session_type}/{session_name}"
    )
    outdir.mkdir(exist_ok=True, parents=True)
    return outdir


def main() -> None:

    vids = find_video_paths(ROOT_DIR)
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
            preprocess(in_path=i, out_dir=output_dir)


if __name__ == "__main__":
    main()
