import re
from os import listdir
from os.path import isfile, join

import pyexiv2


def set_dates(path, filename):
    with open(join(path, filename), encoding="utf-8") as f:
        dates = f.readlines()

    pattern = r"^IMG_\d{4}.jpg$"

    def image_predicate(f):
        return isfile(join(path, f)) and re.search(pattern, f)

    images = sorted([f for f in listdir(path) if image_predicate(f)])

    for i, img_name in enumerate(images):
        full_name = join(path, img_name)

        if i >= len(dates):
            break

        date = dates[i].replace("\n", "")
        if date != "":
            if len(date) == 7:
                day, month, year = "01", date[:2], date[3:]
            elif len(date) == 10:
                day, month, year = date[:2], date[3:5], date[6:]
            else:
                print(f"Invalid date {date}")
                break

            with pyexiv2.Image(full_name) as img:
                formatted_date = f"{year}:{month}:{day} 00:00:00"
                img.modify_exif({"Exif.Photo.DateTimeOriginal": formatted_date})

        print(f'Set date "{formatted_date}" for "{img_name}"')


path = r"D:\OneDrive\Pictures\Scan\Misc\\"
file = "dates.txt"

set_dates(path, file)
