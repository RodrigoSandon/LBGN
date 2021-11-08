from deeplabcut import add_new_videos

CONFIG_PATH = r"/home/rory/repos/ppt_dlc/rdt_sessions-PPT-2021-09-08/config.yaml"


def main():
    videos_list = [
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/74_RDT_D22019-12-04T11_23_50.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/74_RDT_D32019-12-10T14_00_29.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/75_RDT_D12019-11-27T12_14_37.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/102_RDT_D12020-01-15T13_09_14.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/125_RDT_D22020-08-06T10_43_58.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/130_RDT_D32020-08-29T11_57_09.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/134_RDT_D12020-08-10T15_27_25.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/143_RDT_22020-11-03T10_26_51.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/159_RDT_D32020-12-29T10_56_56.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/162_RDT_D12020-12-22T13_05_26.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/75_RDT_D22019-12-06T11_07_26.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/75_RDT_D32019-12-11T12_25_18.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/94_RDT_D12020-01-15T09_48_49.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/94_RDT_D22020-01-22T09_40_53.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/94_RDT_D32020-01-27T09_37_22.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/95_RDT_D12020-01-14T09_59_05.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/95_RDT_D22020-01-22T09_40_53.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/95_RDT_D32020-01-28T09_48_29.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/96_RDT_D12020-01-23T10_36_46.avi",
        "/media/rory/RDT VIDS/DeepLabCut_RDT_Sessions_Only/96_RDT_D22020-01-28T11_28_29.avi",
    ]
    add_new_videos(CONFIG_PATH, videos_list)


if __name__ == "__main__":
    main()
