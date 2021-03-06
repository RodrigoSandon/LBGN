import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


start_path = r"/media/rory/Padlock_DT/BLA_Analysis/BetweenMiceAlignmentData/RDT D2"

list_files(start_path)
