import re
from os import listdir
from os.path import isfile, join

import pyexiv2


def set_titles(path, filename):
    with open(join(path, filename), encoding="utf-8") as f:
        titles = f.readlines()

    pattern = r"^IMG_\d{4}.jpg$"

    def image_predicate(f):
        return isfile(join(path, f)) and re.search(pattern, f)

    images = sorted([f for f in listdir(path) if image_predicate(f)])

    for i, img_name in enumerate(images):
        full_name = join(path, img_name)

        if i >= len(titles):
            break

        title = titles[i].replace("\n", "")
        if title != "":
            with pyexiv2.Image(full_name) as img:
                img.modify_exif(
                    {"Exif.Image.XPTitle": title, "Exif.Image.ImageDescription": title}
                )
                img.modify_xmp({"Xmp.dc.title": title})

        print(f'Set title "{title}" for "{img_name}"')


path = r"D:\OneDrive\Pictures\Scan\Album 2006-10 - 2008-10\\"
file = "titles.txt"

set_titles(path, file)
