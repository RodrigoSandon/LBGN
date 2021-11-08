from pathlib import Path
import os
from typing import List
from preprocess import preprocess

ROOT_DIR = Path(
    r"/media/rory/PTP Inscopix 3/Inscopix_to_Analyze"
)  # change this path to where your videos are stored


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


def main() -> None:
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
            preprocess(in_path=i, out_dir=output_dir)


if __name__ == "__main__":
    main()
