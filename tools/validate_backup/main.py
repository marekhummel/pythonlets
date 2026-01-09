# Checks if all files in DATA are present in BACKUP

import concurrent.futures as cf
import hashlib
import json
import os
import os.path
import shutil
from collections.abc import Iterable, Iterator
from fnmatch import fnmatch
from pathlib import Path
from time import perf_counter
from typing import Any

# Check what files in DATA_PATH (excluding IGNORED) are already present in BACKUP_PATH
DATA_PATH = Path(r"$WINHOME/Downloads/Bilder")
BACKUP_PATH = Path(r"$WINHOME/OneDrive/Pictures")
IGNORED = [
    "**/Thumbs.db",
    "**/.hps-metadata",
    "**/mxfilerelatedcache.mxc2",
    "FOUND.000",
    "System Volume Information",
    ".Spotlight-V100",
]


def get_file_iterator(root: Path) -> Iterator[Path]:
    return (Path(currentpath) / f for currentpath, _, files in os.walk(root) for f in files)


def get_hashdict(file_path: Path, hashlist_path: Path) -> dict[str | None, Path]:
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

    return {v: k for k, v in hashlist.items()}


def compute_file_hash(file: Path) -> str | None:
    BLOCK_SIZE = 65536  # noqa: N806

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


def should_ignore(path: Path, data_path: Path, ignored_patterns: list[str]) -> bool:
    rel_path_str = str(path.relative_to(data_path)).replace("\\", "/")

    return any(fnmatch(rel_path_str, pattern) for pattern in ignored_patterns)


def check_data(
    data_path: Path, hashdict: dict[str | None, Path], ignored: list[str]
) -> list[Path]:
    print("Check files")

    total = 0
    not_found = []
    not_found_count = 0
    with cf.ProcessPoolExecutor() as executor:
        for currentpath, _, files in os.walk(data_path):
            current_path_obj = Path(currentpath)

            # Check if current directory should be ignored
            if should_ignore(current_path_obj, data_path, ignored):
                # print(f" - {current_path_obj.relative_to(data_path)} is skipped")
                continue

            # Filter out ignored files
            fullfiles = [Path(currentpath) / f for f in files]
            fullfiles = [f for f in fullfiles if not should_ignore(f, data_path, ignored)]
            total += len(fullfiles)

            hashed_files = [
                (f, h)
                for f, h in zip(fullfiles, executor.map(compute_file_hash, fullfiles))
                if h is not None
            ]
            current_not_found = [f for f, file_hash in hashed_files if file_hash not in hashdict]

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


def group_files_old(paths: list[tuple[Path, bool]]) -> dict:
    hierarchy: dict = {}

    # Separate directories from files
    directories = [f for f, is_dir in paths if is_dir]
    files = [f for f, is_dir in paths if not is_dir]

    # Group regular files by their first directory component
    files_by_first_dir: dict[str, list[Path]] = {}
    current_level_files: list[str] = []

    for f in files:
        parts = f.parts
        if len(parts) == 0:
            continue
        elif len(parts) == 1:
            # File at current level
            current_level_files.append(parts[0])
        else:
            # File in subdirectory
            first_dir = parts[0]
            if first_dir not in files_by_first_dir:
                files_by_first_dir[first_dir] = []
            files_by_first_dir[first_dir].append(Path(*parts[1:]))

    # Group directories by their first component
    dirs_by_first_component: dict[str, list[Path]] = {}
    current_level_dirs: list[str] = []

    for d in directories:
        parts = d.parts
        if len(parts) == 0:
            continue
        elif len(parts) == 1:
            # Entire directory at this level is missing
            current_level_dirs.append(parts[0])
        else:
            # Subdirectory
            first_dir = parts[0]
            if first_dir not in dirs_by_first_component:
                dirs_by_first_component[first_dir] = []
            dirs_by_first_component[first_dir].append(Path(*parts[1:]))

    # Add files at current level
    if current_level_files:
        hierarchy["%%files%%"] = sorted(current_level_files)

    # Recursively process subdirectories
    all_subdirs = set(files_by_first_dir.keys()) | set(dirs_by_first_component.keys())

    # Add entire directories that are missing at current level (no subdirs)
    for dir_name in sorted(current_level_dirs):
        if dir_name not in all_subdirs:
            # This directory has no subdirectories, mark it as completely missing
            hierarchy[dir_name] = {"%%files%%": "*.*"}

    # Process subdirectories
    for subdir in sorted(all_subdirs):
        subfiles = files_by_first_dir.get(subdir, [])
        subdirs = dirs_by_first_component.get(subdir, [])
        # Create tuples with is_directory flag
        combined = [(f, False) for f in subfiles] + [(d, True) for d in subdirs]
        sub_hierarchy = group_files(combined)

        # If this directory was marked as having all its direct files missing,
        # add that marker to the hierarchy
        if subdir in current_level_dirs:
            sub_hierarchy["%%files%%"] = "*.*"

        hierarchy[subdir] = sub_hierarchy

    return hierarchy


def group_files(paths: Iterable[tuple[Path, bool]]) -> dict[str, Any]:
    files_key = r"%files%"
    default_all_files = "*.*"
    root: dict[str, Any] = {}

    # 1. Build tree structure
    for path, is_dir in paths:
        parts = path.parts
        if not parts:
            continue

        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})

        name = parts[-1]

        if is_dir:
            node.setdefault(name, {})
        else:
            node.setdefault(files_key, []).append(name)

    # 2. Post-process: mark empty directories
    def _mark_empty_dirs(node: dict[str, Any]) -> bool:
        """
        Returns True if this subtree contains any real files.
        """
        has_files = files_key in node and bool(node[files_key])

        for key, child in node.items():
            if key == files_key:
                continue
            if _mark_empty_dirs(child):
                has_files = True

        if not has_files:
            node.setdefault(files_key, [default_all_files])

        return has_files

    _mark_empty_dirs(root)
    return root


if __name__ == "__main__":
    # Start
    start = perf_counter()
    hash_path = Path(r"./tools/validate_backup/hashes.json")
    target_path = Path(r"./tools/validate_backup/not_found.json")
    check_path = Path(r"./tools/validate_backup/check/")

    # Check paths
    if os.path.exists(check_path):
        print("Remove check folder")
        exit(1)

    # Hash backup
    backup_hashes = get_hashdict(BACKUP_PATH, hash_path)

    # Single test
    # h = compute_file_hash(DATA_PATH / "test.jpg")
    # print(backup_hashes.get(h))
    # exit(0)

    # Check all
    files = check_data(DATA_PATH, backup_hashes, IGNORED)

    # Copy not found
    # copy_not_found(DATA_PATH, files, check_path)

    # Create lookup
    # Check if directory BEFORE converting to relative path
    relative_files = [(f.relative_to(DATA_PATH), f.is_dir()) for f in files]
    hierarchy = group_files(relative_files)
    with open(target_path, mode="w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=4, separators=(", ", ": "), sort_keys=True)

    # Done
    print(perf_counter() - start)
