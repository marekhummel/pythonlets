# ruff: noqa: SIM108
import re
from functools import lru_cache
from math import sqrt
from os import listdir
from os.path import exists, isfile, join

from PIL import Image, JpegImagePlugin

DEVIATION_THRESHOLD = 11
BORDER_THRESHOLD = 100000
BORDER_OFFSET = 40


@lru_cache(maxsize=None)
def rgb2lab(red, green, blue):
    rgb = []
    for value in [red, green, blue]:
        value = value / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92
        rgb.append(value * 100)

    # Observer= 2°, Illuminant= D65
    x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    x = x / 95.047  # ref_X =  95.047
    y = y / 100.0  # ref_Y = 100.000
    z = z / 108.883  # ref_Z = 108.883

    xyz = []
    for value in [x, y, z]:
        if value > 0.008856:
            value = value ** (1 / 3)
        else:
            value = (7.787 * value) + (16 / 116)
        xyz.append(value)

    l = 116 * xyz[1] - 16
    a = 500 * (xyz[0] - xyz[1])
    b = 200 * (xyz[1] - xyz[2])

    return (l, a, b)


def avg(l):
    return sum(l) / len(l)


@lru_cache(maxsize=None)
def deviation(rgb):
    white = rgb2lab(255, 255, 255)
    other = rgb2lab(*rgb)
    return sqrt(
        (white[0] - other[0]) ** 2
        + (white[1] - other[1]) ** 2
        + (white[2] - other[2]) ** 2
    )


def crop_whitespace(img_path: str) -> tuple[int, int] | None:
    original = Image.open(img_path)
    width, height = original.size  # Get dimensions

    max_y = height - 1
    while max_y > 0:
        avg_deviation = avg(
            [
                deviation(original.getpixel((x, max_y)))
                for x in range(BORDER_OFFSET, width - BORDER_OFFSET)
            ]
        )
        if avg_deviation > DEVIATION_THRESHOLD:
            break
        max_y -= 1

    if (height - max_y - 1) > BORDER_THRESHOLD:
        max_y = height - 1

    max_x = width - 1
    while max_x > 0:
        avg_deviation = avg(
            [
                deviation(original.getpixel((max_x, y)))
                for y in range(BORDER_OFFSET, height - BORDER_OFFSET)
            ]
        )
        if avg_deviation > DEVIATION_THRESHOLD:
            break
        max_x -= 1

    if (width - max_x - 1) > BORDER_THRESHOLD:
        max_x = width - 1

    crop_box = (0, 0, max_x, max_y)  # bottom
    cropped = original.crop(crop_box)
    quantization = getattr(original, "quantization", None)
    subsampling = JpegImagePlugin.get_sampling(original)
    quality = 100 if quantization is None else -1

    params = {"subsampling": subsampling, "qtables": quantization, "quality": quality}
    exif = original.info.get("exif", None)
    if exif:
        params["exif"] = exif

    new_path = img_path.replace(".jpg", "_crop.jpg")
    try:
        cropped.save(new_path, "JPEG", **params)
        return (width - max_x - 1, height - max_y - 1)
    except ValueError:
        return None
    # cropped.save(img_path.replace('jpg', 'tiff'), 'TIFF', exif=original.info['exif'])


def image_predicate(f):
    return (
        isfile(join(path, f))
        and re.search(pattern, f)
        and not exists(join(path, f.replace(".jpg", "_crop.jpg")))
    )


pattern = r"^IMG_(\d{8})_(\d{4}).jpg$"
# pattern = r'^IMG_\d{8}_0012.jpg$'
path = r"C:\Users\mhummel\Documents\Scanned Documents\Images\\"

images = sorted([f for f in listdir(path) if image_predicate(f)])
for img in images:
    full_name = join(path, img)
    cut = crop_whitespace(full_name)
    print(f'Cropped "{img}" by {cut}')
