# ruff: noqa

import os
import re
from datetime import datetime as dt
from datetime import timedelta
from pprint import pprint

# file = r"D:\OneDrive\Phone Media\Camera Roll\IMG_20220826_212426.jpg"
# stats = os.stat(file)
# print(dt.fromtimestamp(stats.st_atime))
# print(dt.fromtimestamp(stats.st_mtime))
# print(dt.fromtimestamp(stats.st_ctime))


def get_files(base_path, filter_ext: list):
    tree = {}
    parents = {}
    for currentpath, folders, files in os.walk(base_path):
        parents |= {os.path.join(currentpath, d): currentpath for d in folders}
        node


path = r"X:\OneDrive\Pictures\Urlaub"
relevant_ext = [".jpg", ".jpeg", ".png"]

all_files = [
    os.path.join(currentpath, f)
    for currentpath, _, files in os.walk(path)
    for f in files
]
tree = get_files(relevant_ext)
pprint(tree)
exit()

print(f"All: {len(all_files)}")
print()

# relevant = {(f, os.path.splitext(f)[1].lower() in relevant_ext) for f in all_files}
# img_files = {f for f, rel in relevant if rel}
# ignored_files = set(all_files) - img_files

print(f"Img:      {len(relevant_files)}")
print(f"Ignored:  {len(ignored_files)}")
print()


with open("img_dating/relevant.txt", mode="w", encoding="utf-8") as f:
    lst = sorted(f + "\n" for f in relevant_files)
    f.writelines(lst)

with open("img_dating/ignored.txt", mode="w", encoding="utf-8") as f:
    lst = sorted(f + "\n" for f in ignored_files)
    f.writelines(lst)


rgx_renamed = re.compile(
    r"IMG (?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})"
)
rgx_phone_cam = re.compile(
    r"IMG_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})"
)
rgx_whatsapp = re.compile(
    r"IMG-(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-WA(?P<id>\d{4})"
)


renamed_files = {f for f in img_files if rgx_renamed.search(f)}
phonecam_files = {f for f in img_files if rgx_phone_cam.search(f)}
whatsapp_files = {f for f in img_files if rgx_whatsapp.search(f)}
other_files = img_files - renamed_files - phonecam_files - whatsapp_files


print(f"Renamed:   {len(renamed_files)}")
print(f"Phone Cam: {len(phonecam_files)}")
print(f"Whatsapp:  {len(whatsapp_files)}")
print(f"Other:     {len(other_files)}")
print()

error_files = []
for f in phonecam_files:
    match = rgx_phone_cam.search(f)
    vals = {
        g: int(match[g]) for g in ["year", "month", "day", "hour", "minute", "second"]
    }
    filetime = dt(**vals)
    atime = dt.fromtimestamp(os.path.getatime(f))
    ctime = dt.fromtimestamp(os.path.getctime(f))
    mtime = dt.fromtimestamp(os.path.getmtime(f))
    diff = min(abs(filetime - mtime), abs(filetime - ctime), abs(filetime - atime))
    if diff >= timedelta(minutes=1):
        error_files.append([f, filetime, mtime, ctime, atime, diff])

print(f"Error phone cam:     {len(error_files)}")

with open("img_dating/error.csv", mode="w", encoding="utf-8") as fe:
    error_files.sort(key=lambda f: f[5])
    fe.write("file,filetime,mtime,ctime,atime,diff\n")
    for f in error_files:
        fe.write(",".join(str(x).replace(",", "") for x in f) + "\n")


with open("img_dating/other.txt", mode="w", encoding="utf-8") as f:
    lst = sorted(f + "\n" for f in other_files)
    f.writelines(lst)
