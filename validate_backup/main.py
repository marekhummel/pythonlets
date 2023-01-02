# Checks if all files in DATA are present in BACKUP

import concurrent.futures as cf
import hashlib
import json
import os
import os.path
import shutil
from time import perf_counter

BACKUP_PATH = r"D:\OneDrive"
DATA_PATH = "G:\\"
IGNORED = ["FOUND.000", "System Volume Information", ".Spotlight-V100"]


def get_file_iterator(root):
    return (os.path.join(currentpath, f) for currentpath, _, files in os.walk(root) for f in files)


def get_hashdict(file_path, hashlist_path):
    print("Update hashdict")
    all_files = list(get_file_iterator(file_path))

    hashlist = {}
    if os.path.exists(hashlist_path):
        with open(hashlist_path, "r") as f:
            hashlist = json.load(f)

    with cf.ProcessPoolExecutor() as executor:
        new_files = set(all_files) - set(hashlist.keys())
        for f, file_hash in zip(new_files, executor.map(compute_file_hash, new_files)):
            hashlist[f] = file_hash

    print(f"Created hashlist with {len(hashlist)} entries")
    with open(hashlist_path, "w") as f:
        json.dump(hashlist, f)
    return set(hashlist.values())


def compute_file_hash(file):
    BLOCK_SIZE = 65536

    file_hash = hashlib.md5()
    try:
        with open(file, "rb") as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)

        return file_hash.hexdigest()
    except OSError:
        print(f"Hashing failed: {file}")
        return None


def check_data(path, hashset, ignored):
    print("Check files")
    abs_ignored = [os.path.join(path, i) for i in ignored]

    total = 0
    not_found = []
    not_found_count = 0
    with cf.ProcessPoolExecutor() as executor:
        for currentpath, _, files in os.walk(path):
            if currentpath in abs_ignored:
                print(f" - {currentpath} is skipped")
                continue

            fullfiles = [os.path.join(currentpath, f) for f in files]
            total += len(fullfiles)

            hashed_files = [
                (f, h) for f, h in zip(fullfiles, executor.map(compute_file_hash, fullfiles)) if h is not None
            ]
            current_not_found = [f for f, file_hash in hashed_files if file_hash not in hashset]

            not_found_count += len(current_not_found)
            if len(current_not_found) == len(hashed_files) and current_not_found:
                not_found.append(f"{currentpath}\\*.*")
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


def group_files(files):
    split_files = [f.rstrip().split("\\", 1) for f in files]

    groups = {}
    files = []
    for f in split_files:
        if len(f) == 1:
            files.append(f[0])
        else:
            grp = f[0]
            if grp not in groups:
                groups[grp] = []
            groups[grp].append(f[1])

    hierarchy = {}
    if files:
        hierarchy["%%files%%"] = files
    for g, vals in groups.items():
        hierarchy[g] = group_files(vals)

    return hierarchy


if __name__ == "__main__":
    # Start
    start = perf_counter()
    hash_path = r".\validate_backup\hashes.json"
    target_path = r".\validate_backup\not_found.json"
    check_path = r".\validate_backup\check\\"

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
    hierarchy = group_files(files)
    with open(target_path, mode="w") as f:
        json.dump(hierarchy, f, indent=4, separators=(", ", ": "), sort_keys=True)

    # Done
    print(perf_counter() - start)
