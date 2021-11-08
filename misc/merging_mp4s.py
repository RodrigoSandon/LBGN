import os
import glob
from pathlib import Path


def delete_recursively(root, name_endswith_list):

    for i in name_endswith_list:

        files = glob.glob(os.path.join(root, "**", "*%s") % (i), recursive=True)

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


def delete_recursively_test(root, name_endswith):

    files = glob.glob(os.path.join(root, "**", "*%s") % (name_endswith), recursive=True)

    for f in files:
        if name_endswith in f:
            print(f)
            try:
                os.remove(f)
                pass
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


def main():
    count = 0
    ROOT_PATH = Path(r"/media/rory/RDT VIDS/RRD ChrimsonR Approach Aborts")

    delete_recursively(ROOT_PATH, "mylist.txt")

    for root, dir, files in os.walk(ROOT_PATH):
        # change working directory
        os.chdir(root)
        print("Current working dir: ", os.getcwd())
        count += 1

        do_process = True
        for name in files:
            if ("mylist.txt" or "_merged.mp4") in name:
                do_process = False

        if do_process == True:
            # open new text file
            file = open("mylist.txt", "w")
            name_merged_file = ""
            L = []
            for name in files:
                if (".MP4") in name:
                    os.rename(name, name.replace(" ", "_"))
                    os.rename(name, name.replace("(", "_").replace(")", "_"))
                    # print(name)
                    name_merged_file = name.replace(".MP4", "")
                    name_str = "file '%s'" % (name) + "\n"
                    L.append(name_str)

            file.writelines(L)
            file.close()
            # have the input file written now
            if name_merged_file != "":
                cmd = "ffmpeg -f concat -safe 0 -i mylist.txt -c copy %s_merged.mp4" % (
                    name_merged_file
                )
                print(cmd)
                os.system(cmd)


def delete_old_mp4s():
    ROOT_PATH = Path(r"/media/rory/RDT VIDS/RRD ChrimsonR Approach Aborts")
    delete_recursively_test(ROOT_PATH, "_.MP4")


main()
delete_old_mp4s()
