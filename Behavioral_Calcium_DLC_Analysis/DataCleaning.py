import os, glob
import shutil
import re


def dir_del_recursively(foldername, root) -> None:
    # all_betweencell_alignment_folders = []
    deleted = 0
    for path, dirs, files in os.walk(root):
        if foldername in dirs:
            shutil.rmtree(os.path.join(path, foldername))
            # all_betweencell_alignment_folders.append(os.path.join(path, foldername))
            deleted += 1
        print(deleted)
    print("Number of BetweenCellAlignmentData folders deleted:", deleted)


ROOT = r"/media/rory/Padlock_DT/BLA_Analysis"

# dir_del_recursively("BetweenCellAlignmentData", ROOT)
def delete_recursively(root_path, name_endswith_list):

    for i in name_endswith_list:

        files = glob.glob(os.path.join(root_path, "**", "*%s") % (i), recursive=True)

        for f in files:
            try:
                os.remove(f)
                print("Removed ", f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            # os.remove(os.pah.join(dir,f))
            print(os.path.join(dir, f))


del_list = ["see_if_right.txt", "categorized_cell_avg_traces.txt"]

delete_recursively(ROOT, del_list)
