import re
from os import listdir, rename
from os.path import isfile, join


def image_predicate(f):
    return isfile(join(path, f)) and re.search(pattern, f)


path = r"D:\OneDrive\Pictures\Scan\Sammelbuch\Tickets"
pattern = r"^IMG_(\d{4}).jpg$"

images = sorted([f for f in listdir(path) if image_predicate(f)], reverse=False)

for f in images:
    full = join(path, f)
    i = re.match(pattern, f).group(1)

    if int(i) > 16:
        new_name = f"IMG_{int(i) + -1:04d}.jpg"
        rename(full, join(path, new_name))
        print(f, new_name)
