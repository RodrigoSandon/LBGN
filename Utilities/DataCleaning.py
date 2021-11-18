import os, glob


def delete_recursively(self, name_endswith_list):

    for i in name_endswith_list:

        files = glob.glob(
            os.path.join(self.root_path, "**", "*%s") % (i), recursive=True
        )

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
