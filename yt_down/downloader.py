import re
import shutil
from os import walk
from os.path import splitext

from pytube import Playlist, YouTube
from pytube.helpers import safe_filename


def download_playlist(uri, target, ignore_rgx):
    pl = Playlist(uri)
    pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    for link in pl:
        download_video(link, target, ignore_rgx)


def download_video(uri, target, ignore_rgx='(?!)'):
    cols = shutil.get_terminal_size()[0] - 1

    tries = 0
    while tries < 5:
        try:
            print(f'Attempting "{uri}".', end="\r")
            yt = YouTube(uri)
            all_files = rec_files(target)
            if re.match(ignore_rgx, yt.title):
                print(f'"{yt.title}" ignored.'.ljust(cols))
                return
            if safe_filename(yt.title) in all_files:
                print(f'"{yt.title}" skipped.'.ljust(cols))
                return
            print(f'"{yt.title}" downloading...'.ljust(cols), end='\r')
            yt.streams.get_highest_resolution().download(target)
            print(f'"{yt.title}" done.'.ljust(cols))
            break
        except:
            tries += 1
    else:
        print(f'"{uri}" failed.'.ljust(cols))


def rec_files(path):
    for _, _, filenames in walk(path):
        for filename in filenames:
            yield splitext(filename)[0]
