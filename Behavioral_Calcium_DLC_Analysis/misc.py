import os
import os.path as path


def walk(top, topdown=True, onerror=None, followlinks=False, maxdepth=None):
    islink, join, isdir = path.islink, path.join, path.isdir

    try:
        names = os.listdir(top)
    except OSError as err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs

    if maxdepth is None or maxdepth > 1:
        for name in dirs:
            new_path = join(top, name)
            if followlinks or not islink(new_path):
                for x in walk(
                    new_path,
                    topdown,
                    onerror,
                    followlinks,
                    None if maxdepth is None else maxdepth - 1,
                ):
                    yield x
    if not topdown:
        yield top, dirs, nondirs


session_count = 0
for root, dirs, files in walk("/media/rory/Padlock_DT/BLA_Analysis", maxdepth=4):
    print(root)
