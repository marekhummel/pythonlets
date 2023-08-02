""" Shrinks mp4 video to given maxsize with ffmpeg """

import os
import subprocess
from pathlib import Path

PATH = r".//"
MAXSIZE_MB = 5

# --------------------------------

maxsize_b = MAXSIZE_MB * 1000 * 1000
maxsize_mib = maxsize_b / 1024 / 1024 * 0.98
directory = Path(PATH)

print(directory.name)
for file in list(directory.iterdir()):
    if not file.is_file() or not file.suffix == ".mp4":
        print(f"Skipping {file.name}, no video")
        continue

    fs = file.stat().st_size
    if fs <= maxsize_b:
        print(f"Skipping {file.name}, already small enough")
        continue

    print(f"Starting {file.name}...", end="")
    new_file = str(file).replace(".mp4", "_shrink.mp4")
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            str(file),
            "-vcodec",
            "libx265",
            "-crf",
            "28",
            "-fs",
            f"{maxsize_mib:.2f}M",
            new_file,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    os.rename(file, str(file).replace(".mp4", "_orig.mp4"))
    os.rename(new_file, file)
    print(" done")
