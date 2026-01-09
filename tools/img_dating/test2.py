import os


def get_full_tree(base_path, filter_ext: list):
    tree = {".": None}
    total = 0

    for current_path, folders, files in os.walk(base_path):
        rel_path = current_path.replace(base_path, ".")
        node_names = rel_path.split(os.path.sep)

        node = tree
        for name in node_names[:-1]:
            node = node[name][0]

        entry = (
            {f: None for f in folders},
            len([f for f in files if os.path.splitext(f)[1].lower() in filter_ext]),
        )
        total += len(files)
        node[node_names[-1]] = entry

    print(total)
    return tree


def write_tree(fhndl, tree, indent=0):
    for key, value in tree.items():
        folders, files = value

        fhndl.write(" " * indent + key + f" ({files} file/s)\n")
        write_tree(fhndl, folders, indent=indent + 4)


path = r"X:\OneDrive\Pictures"
relevant_ext = [".jpg", ".jpeg", ".png"]

# all_files = [
#     os.path.join(currentpath, f)
#     for currentpath, _, files in os.walk(path)
#     for f in files
# ]
tree = get_full_tree(path, relevant_ext)
with open("img_dating/all.txt", mode="w", encoding="utf-8") as f:
    write_tree(f, tree)

exit()

# print(f"All: {len(all_files)}")
# print()
