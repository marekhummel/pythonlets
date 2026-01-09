import re
import shutil

from pytubefix import Playlist, YouTube


def download_playlist(uri, target, audio_only, ignore_rgx):
    pl = Playlist(uri)
    pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    for link in pl:
        download_video(link, target, audio_only, ignore_rgx)


def download_video(uri, target, audio_only=False, ignore_rgx="(?!)"):
    cols = shutil.get_terminal_size()[0] - 1

    try:
        print(f'Attempting "{uri}".', end="\r")
        yt = YouTube(uri)

        if re.match(ignore_rgx, yt.title):
            print(f'"{yt.title}" ignored.'.ljust(cols))
            return

        print(f'"{yt.title}" downloading...'.ljust(cols), end="\r")

        if audio_only:
            stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        else:
            stream = yt.streams.get_highest_resolution()
        stream.download(target, skip_existing=True, max_retries=3)

        print(f'"{yt.title}" done.'.ljust(cols))
    except Exception as e:  # noqa
        print(f'"{uri}" failed ({e}).'.ljust(cols))
