# Given a video mp4 (no audio) and an audio mp4 (no video), merge to one
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from os import mkdir, rename

# ------

path = r"D:\UserFolders\Downloads\dwhelper\\"
title = "Intelligenz"
# mkdir(path + title)


for i in range(14):
    video = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i*2}.mp4"

    if i == 0:
        video = video.replace("-0.mp4", ".mp4")
    audio = f"»{title}« Die ZEIT Akademie - Seminar Player www.zeitakademie.de-{i*2 + 1}.mp4"
    target = f"{title} - Lektion {i+1:02d}.mp4"
    print("Merge:", target)
    ffmpeg_merge_video_audio(path + video, path + audio, path + title + "\\" + target, logger=None)
