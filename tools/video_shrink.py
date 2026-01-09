"""Shrinks mp4 video to given maxsize with ffmpeg"""

import os
import subprocess
import sys
from pathlib import Path

PATH = sys.argv[1]  # r"D:\UserFolders\Videos\Valorant"
MAXSIZE_MB = 40

# --------------------------------

maxsize_b = MAXSIZE_MB * 1000 * 1000
maxsize_mib = maxsize_b / 1024 / 1024 * 0.98
directory = Path(PATH)


def parse(file: Path):
    if not file.is_file() or file.suffix != ".mp4":
        print(f"Skipping {file.name}, no video")
        return

    if file.stem.endswith("_orig"):
        print(f"Skipping {file.name}, already shrunk")
        return

    fs = file.stat().st_size
    if fs <= maxsize_b * 100 / MAXSIZE_MB:
        print(f"Skipping {file.name}, already small enough")
        return

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


if __name__ == "__main__":
    print(directory.name)
    for file in list(directory.iterdir()):
        parse(file)
    print("Done with all")
