# Checks if all files in DATA are present in BACKUP

import concurrent.futures as cf
import hashlib
import json
import os
import os.path
import shutil
from time import perf_counter
from pathlib import Path
from typing import Any, Iterator

DATA_PATH = Path(r"D:\OneDrive\Phone Media\WhatsApp")
BACKUP_PATH = Path(r"D:\OneDrive\Pictures")
IGNORED = []  # ["FOUND.000", "System Volume Information", ".Spotlight-V100"]


def get_file_iterator(root: Path) -> Iterator[Path]:
    return (Path(currentpath) / f for currentpath, _, files in os.walk(root) for f in files)


def get_hashdict(file_path: Path, hashlist_path: Path) -> set[str | None]:
    print(f"Update hashdict of {file_path}")
    all_files = list(get_file_iterator(file_path))

    hashlist: dict[Path, str | None] = {}
    if hashlist_path.exists():
        with hashlist_path.open("r") as f:
            hashes = json.load(f)
            hashlist = {Path(p): h for p, h in hashes.items()}

    with cf.ProcessPoolExecutor() as executor:
        new_files = set(all_files) - set(hashlist.keys())
        for file, file_hash in zip(new_files, executor.map(compute_file_hash, new_files)):
            hashlist[file] = file_hash

    print(f"Created hashlist with {len(hashlist)} entries")
    with hashlist_path.open("w", encoding="utf-8") as f:
        json.dump({str(p): h for p, h in hashlist.items()}, f)

    return set(hashlist.values())


def compute_file_hash(file: Path) -> str | None:
    BLOCK_SIZE = 65536

    file_hash = hashlib.md5()
    try:
        with file.open("rb") as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)

        return file_hash.hexdigest()
    except OSError:
        print(f"Hashing failed: {file}")
        return None


def check_data(data_path: Path, hashset: set[str | None], ignored: list[str]) -> list[Path]:
    print("Check files")
    abs_ignored = [os.path.join(data_path, i) for i in ignored]

    total = 0
    not_found = []
    not_found_count = 0
    with cf.ProcessPoolExecutor() as executor:
        for currentpath, _, files in os.walk(data_path):
            if currentpath in abs_ignored:
                print(f" - {currentpath} is skipped")
                continue

            fullfiles = [Path(currentpath) / f for f in files]
            total += len(fullfiles)

            hashed_files = [
                (f, h) for f, h in zip(fullfiles, executor.map(compute_file_hash, fullfiles)) if h is not None
            ]
            current_not_found = [f for f, file_hash in hashed_files if file_hash not in hashset]

            not_found_count += len(current_not_found)
            if len(current_not_found) == len(hashed_files) and current_not_found:
                # not_found.append(f"{currentpath}\\*.*")
                not_found.append(Path(currentpath))
            else:
                not_found.extend(current_not_found)

    print(f"{not_found_count} of {total} files not found.")
    return not_found


def copy_not_found(root, files, check_path):
    print("Copy missing data")
    os.mkdir(check_path)

    for f in files:
        target = f.replace(root, check_path)

        if f.endswith("*.*"):
            shutil.copytree(f.replace("*.*", ""), target.replace("*.*", ""), dirs_exist_ok=True)
        else:
            folder = target[: target.rindex("\\")]
            if not os.path.exists(folder):
                os.makedirs(folder)
            shutil.copy2(f, target)


def group_files(files: list[str]) -> dict:
    split_files = [f.rstrip().split("\\", 1) for f in files]

    groups: dict[str, list[str]] = {}
    curr_files: list[str] = []
    for f in split_files:
        if len(f) == 1:
            curr_files.append(f[0])
        else:
            grp = f[0]
            if grp not in groups:
                groups[grp] = []
            groups[grp].append(f[1])

    hierarchy: dict = {}
    if curr_files:
        hierarchy["%%files%%"] = curr_files
    for g, vals in groups.items():
        hierarchy[g] = group_files(vals)

    return hierarchy


if __name__ == "__main__":
    # Start
    start = perf_counter()
    hash_path = Path(r".\tools\validate_backup\hashes.json")
    target_path = Path(r".\tools\validate_backup\not_found.json")
    check_path = Path(r".\tools\validate_backup\check\\")

    # Check paths
    if os.path.exists(check_path):
        print("Remove check folder")
        exit(1)

    # Check
    backup_hashes = get_hashdict(BACKUP_PATH, hash_path)
    files = check_data(DATA_PATH, backup_hashes, IGNORED)

    # Copy not found
    # copy_not_found(DATA_PATH, files, check_path)

    # Create lookup
    hierarchy = group_files([str(p) for p in files])
    with open(target_path, mode="w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=4, separators=(", ", ": "), sort_keys=True)

    # Done
    print(perf_counter() - start)
