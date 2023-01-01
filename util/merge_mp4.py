# Given a video mp4 (no audio) and an audio mp4 (no video), merge to one
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from os import mkdir, rename

# ------

path = r"D:\UserFolders\Downloads\dwhelper\\"
title = "Das Einmaleins für Finanzen"
mkdir(path + title)
mkdir(path + title + "\\Lektionen")


for i in range(9):
    video = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i*2}.mp4"

    if i == 0:
        video = video.replace("-0.mp4", ".mp4")
    audio = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i*2 + 1}.mp4"
    target = f"{title} - Lektion {i+1:02d}.mp4"
    print("Merge:", target)
    ffmpeg_merge_video_audio(path + video, path + audio, path + title + "\\Lektionen\\" + target, logger=None)

# ------


# for i in range(13, 21, +1):
#     file = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i}.mp4"
#     new_file = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i-1}.mp4"

#     rename(path + file, path + new_file)
