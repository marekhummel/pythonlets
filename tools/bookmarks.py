""" Extracts links from firefox bookmarks json """

from collections import namedtuple
import json
import re

Uri = namedtuple("Uri", ["title", "uri"])


def parse_tree(tree):
    t = tree["type"]
    if t == "text/x-moz-place-container":
        # folder
        subtrees = [parse_tree(st) for st in tree.get("children", [])]
        return [uri for st in subtrees for uri in st]
    elif t == "text/x-moz-place":
        # uri
        return [Uri(re.sub(r"[^ \w+]", " ", tree["title"]), tree["uri"])]
    elif t == "text/x-moz-place-separator":
        # sep
        return []

    print("wdf")


with open("./firefox-bookmarks-2023-07-05.json", encoding="utf-8") as f:
    data = json.load(f)

uris = parse_tree(data)

longest_title = max([len(u.title) for u in uris])
with open("./firefox-bookmarks.txt", mode="w+", encoding="utf-8") as f:
    f.writelines([f"{u.title.ljust(longest_title + 2)}: {u.uri}\n" for u in uris])
# print(uris)
