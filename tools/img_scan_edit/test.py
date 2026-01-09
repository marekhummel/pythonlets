from os import listdir, rename
from os.path import isfile, join

path = r"D:\UserFolders\Documents\Scanned Documents\Images"
images = sorted([f for f in listdir(path) if isfile(join(path, f))])

i = 1
for f in images:
    full = join(path, f)
    new_name = f"IMG_{int(i):04d}.jpg"
    rename(full, join(path, new_name))
    print(f, new_name)

    i += 1
