from deeplabcut import plot_trajectories
from pathlib import Path
from typing import List

CONFIG_PATH = r"/home/rory/repos/ppt_dlc/rdt_sessions-PPT-2021-09-08/config.yaml"


def find_video_paths(
    raw_data_parent_dir: Path, dir_of_vids_for_training: Path
) -> List[str]:

    videos_of_training = [
        str(vid) for i, vid in enumerate(dir_of_vids_for_training.glob("*.avi"))
    ]
    return [
        str(vid)
        for i, vid in enumerate(raw_data_parent_dir.glob("*.avi"))
        if str(vid) not in videos_of_training
    ]


RAW_DATA_DIR = Path(r"/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only")
VIDS_OF_TRAINING = Path(r"/home/rory/repos/ppt_dlc/rdt_sessions-PPT-2021-09-08/videos")
video_paths = find_video_paths(RAW_DATA_DIR, dir_of_vids_for_training=VIDS_OF_TRAINING)


def main():
    print("Plotting: ", video_paths[3])
    plot_trajectories(CONFIG_PATH, video_paths[3])


if __name__ == "__main__":
    main()
